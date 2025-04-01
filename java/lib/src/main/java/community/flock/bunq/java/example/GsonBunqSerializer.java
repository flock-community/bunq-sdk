package community.flock.bunq.java.example;

import com.bunq.sdk.json.BunqGsonBuilder;
import com.google.gson.Gson;
import community.flock.bunq.java.BunqModelCopied;
import community.flock.bunq.java.BunqSerializer;

import java.lang.reflect.Type;
import java.util.Optional;

public class GsonBunqSerializer implements BunqSerializer {
    private final Gson gson = BunqGsonBuilder.buildDefault()
            .registerTypeAdapter(Optional.class, new BunqModelCopied.OptionalSerializer())
            .registerTypeAdapter(Optional.class, new BunqModelCopied.OptionalDeserializer<>())
            .create();

    @Override
    public <T> String serialize(T t, Type type) {
        return gson.toJson(t, type);
    }

    @Override
    public <T> T deserialize(String raw, Type type) {
        return gson.fromJson(raw, type);
    }
}
