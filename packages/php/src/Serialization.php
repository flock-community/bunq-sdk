<?php

declare(strict_types=1);

namespace Bunq\Sdk;

use Bunq\Api\Wirespec;

/**
 * JSON for the generated client. The type of a value is the PHPDoc type string the generated code passes, such as
 * `'int'`, `Payment::class` or `'list<' . Payment::class . '>'`; a model is built through its constructor, reading
 * the types of its list and dict fields from the constructor's `@param` tags.
 *
 * bunq wraps a result in `{"Response": [{"Payment": {...}}, ...]}`: a single result merges the objects in the
 * list, a list result takes the value of each, and a page keeps the items together with the `Pagination` block.
 * An error response has no envelope: the document itself is the body.
 */
final class Serialization implements Wirespec\Serialization
{
    private const JSON_FLAGS = \JSON_THROW_ON_ERROR | \JSON_UNESCAPED_SLASHES | \JSON_UNESCAPED_UNICODE | \JSON_PRESERVE_ZERO_FRACTION;

    /** @var array<class-string, list<array{name: string, type: string, optional: bool}>> */
    private static array $constructors = [];

    public function serializeBody(mixed $t, string $type): string
    {
        return $t === null ? '' : \json_encode(self::normalize($t), self::JSON_FLAGS);
    }

    public function deserializeBody(string $raw, string $type): mixed
    {
        $document = \json_decode($raw, true, 512, \JSON_THROW_ON_ERROR);
        if (!\is_array($document) || \array_is_list($document) && $document !== []) {
            throw new \UnexpectedValueException('Invalid bunq response: neither Response nor Error');
        }
        if (!\array_key_exists('Response', $document)) {
            return \array_key_exists('Error', $document)
                ? self::hydrate($type, $document)
                : throw new \UnexpectedValueException('Invalid bunq response: neither Response nor Error');
        }
        $items = $document['Response'];
        $values = \array_map(static fn (array $item): mixed => \reset($item), $items);
        return match (true) {
            \array_key_exists('Pagination', $document) => self::hydrate($type, ['Response' => $values, 'Pagination' => $document['Pagination']]),
            \str_starts_with($type, 'list<') => self::hydrate($type, $values),
            default => self::hydrate($type, \array_merge([], ...$items)),
        };
    }

    public function serializePath(mixed $t, string $type): string
    {
        return self::scalar($t);
    }

    public function deserializePath(string $raw, string $type): mixed
    {
        return self::fromString($raw, $type);
    }

    public function serializeParam(mixed $value, string $type): array
    {
        return \is_array($value) ? \array_map(self::scalar(...), \array_values($value)) : [self::scalar($value)];
    }

    public function deserializeParam(array $values, string $type): mixed
    {
        return \preg_match('/^list<(.+)>$/', $type, $list) === 1
            ? \array_map(static fn (string $value): mixed => self::fromString($value, $list[1]), $values)
            : self::fromString($values[0] ?? throw new \UnexpectedValueException("No value for $type"), $type);
    }

    /** The JSON value of a model, enum or refined value; null fields are left out. */
    private static function normalize(mixed $value): mixed
    {
        return match (true) {
            $value instanceof \BackedEnum => $value->value,
            $value instanceof Wirespec\Refined => self::normalize($value->value),
            \is_object($value) => (object) \array_map(self::normalize(...), \array_filter(\get_object_vars($value), static fn (mixed $field): bool => $field !== null)),
            \is_array($value) => \array_map(self::normalize(...), $value),
            default => $value,
        };
    }

    private static function scalar(mixed $value): string
    {
        return match (true) {
            $value instanceof \BackedEnum => (string) $value->value,
            $value instanceof Wirespec\Refined => self::scalar($value->value),
            \is_bool($value) => $value ? 'true' : 'false',
            \is_scalar($value), $value instanceof \Stringable => (string) $value,
            default => throw new \UnexpectedValueException('Cannot write a ' . \get_debug_type($value) . ' as a path segment or parameter'),
        };
    }

    private static function fromString(string $raw, string $type): mixed
    {
        $type = \ltrim($type, '?');
        return match (true) {
            $type === 'int' => (int) $raw,
            $type === 'float' => (float) $raw,
            $type === 'bool' => $raw === 'true',
            \in_array($type, ['string', 'mixed'], true) => $raw,
            default => self::hydrate($type, $raw),
        };
    }

    /** Builds the value of the PHPDoc type from decoded JSON; short class names resolve against $namespace. */
    private static function hydrate(string $type, mixed $value, string $namespace = ''): mixed
    {
        $type = \trim($type);
        $nullable = \str_starts_with($type, '?') || \str_ends_with($type, '|null');
        $type = $nullable ? \preg_replace('/^\?|\|null$/', '', $type) : $type;
        return match (true) {
            $value === null => $nullable || $type === 'mixed' ? null : throw new \UnexpectedValueException("Missing value of type $type"),
            $type === 'mixed' => $value,
            \preg_match('/^list<(.+)>$/s', $type, $list) === 1 =>
                \array_map(static fn (mixed $element): mixed => self::hydrate($list[1], $element, $namespace), \array_values(self::array($value, $type))),
            \preg_match('/^array<\s*[^,<>]+,(.+)>$/s', $type, $dict) === 1 =>
                \array_map(static fn (mixed $entry): mixed => self::hydrate($dict[1], $entry, $namespace), self::array($value, $type)),
            $type === 'int' => \is_int($value) || \is_string($value) && \is_numeric($value) ? (int) $value : self::mismatch($type, $value),
            $type === 'float' => \is_int($value) || \is_float($value) || \is_string($value) && \is_numeric($value) ? (float) $value : self::mismatch($type, $value),
            $type === 'string' => \is_scalar($value) ? (string) $value : self::mismatch($type, $value),
            $type === 'bool' => \is_bool($value) ? $value : self::mismatch($type, $value),
            default => self::object(self::resolve($type, $namespace), $value),
        };
    }

    /**
     * @param class-string $class
     */
    private static function object(string $class, mixed $value): object
    {
        if (\is_subclass_of($class, \BackedEnum::class)) {
            return $class::from($value);
        }
        if (!\is_array($value) && !\is_subclass_of($class, Wirespec\Refined::class)) {
            self::mismatch($class, $value);
        }
        $namespace = \substr($class, 0, (int) \strrpos($class, '\\'));
        $arguments = [];
        foreach (self::constructor($class) as ['name' => $name, 'type' => $type, 'optional' => $optional]) {
            $field = \is_subclass_of($class, Wirespec\Refined::class) ? $value : ($value[$name] ?? null);
            if ($field === null && $optional) {
                continue;
            }
            $arguments[$name] = self::hydrate($type, $field, $namespace);
        }
        return new $class(...$arguments);
    }

    /**
     * The parameters of the constructor, typed by their `@param` tag where it has one.
     *
     * @param class-string $class
     * @return list<array{name: string, type: string, optional: bool}>
     */
    private static function constructor(string $class): array
    {
        return self::$constructors[$class] ??= (static function () use ($class): array {
            $constructor = (new \ReflectionClass($class))->getConstructor()
                ?? throw new \UnexpectedValueException("$class has no constructor to deserialize into");
            \preg_match_all('/@param\s+(.+?)\s+\$(\w+)\s*$/m', (string) $constructor->getDocComment(), $tags, \PREG_SET_ORDER);
            $documented = \array_column($tags, 1, 2);
            return \array_map(static fn (\ReflectionParameter $parameter): array => [
                'name' => $parameter->getName(),
                'type' => $documented[$parameter->getName()] ?? self::nativeType($parameter),
                'optional' => $parameter->isOptional(),
            ], $constructor->getParameters());
        })();
    }

    private static function nativeType(\ReflectionParameter $parameter): string
    {
        $type = $parameter->getType();
        return match (true) {
            !$type instanceof \ReflectionNamedType => 'mixed',
            $type->allowsNull() && $type->getName() !== 'mixed' && $type->getName() !== 'null' => '?' . $type->getName(),
            default => $type->getName(),
        };
    }

    /** @return class-string */
    private static function resolve(string $type, string $namespace): string
    {
        $name = \ltrim($type, '\\');
        $candidates = $namespace === '' ? [$name] : [$name, "$namespace\\$name"];
        foreach ($candidates as $candidate) {
            if (\class_exists($candidate) || \enum_exists($candidate)) {
                return $candidate;
            }
        }
        throw new \UnexpectedValueException("Unknown type $type");
    }

    /** @return array<array-key, mixed> */
    private static function array(mixed $value, string $type): array
    {
        return \is_array($value) ? $value : self::mismatch($type, $value);
    }

    private static function mismatch(string $type, mixed $value): never
    {
        throw new \UnexpectedValueException("Expected $type, got " . \get_debug_type($value));
    }
}
