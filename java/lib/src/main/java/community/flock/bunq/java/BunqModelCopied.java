package community.flock.bunq.java;

import com.bunq.sdk.http.BunqResponse;
import com.bunq.sdk.json.BunqGsonBuilder;
import com.google.gson.Gson;
import com.google.gson.JsonDeserializationContext;
import com.google.gson.JsonDeserializer;
import com.google.gson.JsonElement;
import com.google.gson.JsonNull;
import com.google.gson.JsonObject;
import com.google.gson.JsonParseException;
import com.google.gson.JsonSerializationContext;
import com.google.gson.JsonSerializer;

import java.lang.reflect.ParameterizedType;
import java.lang.reflect.Type;
import java.util.Optional;


abstract public class BunqModelCopied {

    /**
     * Field constants.
     */
    private static final String FIELD_RESPONSE = "Response";

    /**
     * Index of the very first item in an array.
     */
    private static final int INDEX_FIRST = 0;


    /**
     * Gson builder for serialization.
     */
    protected static Gson gson;

    static {
        // Initialize Gson with custom TypeAdapter for Optional
        gson = BunqGsonBuilder
                .buildDefault()
                .registerTypeAdapter(Optional.class, new OptionalSerializer())
                .registerTypeAdapter(Optional.class, new OptionalDeserializer<>())
                .create();

    }

    protected BunqModelCopied() {
    }

    // Custom serializer for Optional
    public static class OptionalSerializer implements JsonSerializer<Optional<?>> {
        @Override
        public JsonElement serialize(Optional<?> src, Type typeOfSrc, JsonSerializationContext context) {
            return src.isPresent() ? context.serialize(src.get()) : JsonNull.INSTANCE;
        }
    }

    // Fix for `OptionalDeserializer` Deserialization Recursion
    public static class OptionalDeserializer<T> implements JsonDeserializer<Optional<T>> {
        @Override
        public Optional<T> deserialize(JsonElement json, Type typeOfT, JsonDeserializationContext context) throws JsonParseException {
            if (json.isJsonNull()) {
                return Optional.empty();
            }

            // Properly resolve the inner type of Optional
            Type actualType = resolveOptionalType(typeOfT);
            T value = context.deserialize(json, actualType);
            return Optional.ofNullable(value);
        }

        /**
         * Resolves the actual generic type inside Optional<T>.
         */
        private Type resolveOptionalType(Type typeOfT) {
            if (typeOfT instanceof ParameterizedType) {
                return ((ParameterizedType) typeOfT).getActualTypeArguments()[0];
            }
            throw new JsonParseException("Type is not parameterized: " + typeOfT.toString());
        }
    }

    private static JsonObject getResponseItemObject(BunqResponseRaw responseRaw) {
        JsonObject responseItemObject = deserializeResponseObject(responseRaw);

        return responseItemObject.getAsJsonArray(FIELD_RESPONSE).get(INDEX_FIRST).getAsJsonObject();
    }

    private static JsonObject getWrappedContent(JsonObject json, String wrapper) {
        return json.getAsJsonObject(wrapper);
    }


    public static String fromJsonToRawResponse(BunqResponseRaw responseRaw,
                                               String wrapper) {
        JsonObject responseItemObject = getResponseItemObject(responseRaw);
        JsonObject asJsonObject = responseItemObject.getAsJsonObject(wrapper);
        return gson.toJson(asJsonObject);

    }

    public static String fromJsonToRawResponse(BunqResponseRaw responseRaw) {
        JsonObject responseItemObject = getResponseItemObject(responseRaw);
        return gson.toJson(responseItemObject);

    }

    /**
     * De-serialize an object from JSON.
     */
    public static <T> BunqResponse<T> fromJson(Class<T> classOfObject, BunqResponseRaw responseRaw,
                                               String wrapper) {
        JsonObject responseItemObject = getResponseItemObject(responseRaw);
        JsonObject responseItemObjectUnwrapped = getWrappedContent(responseItemObject, wrapper);
        T responseValue = gson.fromJson(responseItemObjectUnwrapped, classOfObject);

        return new BunqResponse<>(responseValue, responseRaw.getHeaders());
    }

    public static <T> BunqResponse<T> fromJson(Class<T> classOfObject,
                                               BunqResponseRaw responseRaw) {
        JsonObject responseItemObject = getResponseItemObject(responseRaw);
        T responseValue = gson.fromJson(responseItemObject, classOfObject);

        return new BunqResponse<>(responseValue, responseRaw.getHeaders());
    }

    /**
     * De-serializes a list from JSON.
     */


    protected static JsonObject deserializeResponseObject(BunqResponseRaw responseRaw) {
        String json = new String(responseRaw.getBodyBytes());

        return gson.fromJson(json, JsonObject.class);
    }


}
