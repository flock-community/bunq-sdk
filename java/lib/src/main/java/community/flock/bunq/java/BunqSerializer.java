package community.flock.bunq.java;

import community.flock.wirespec.java.Wirespec;
import community.flock.wirespec.java.serde.DefaultParamSerialization;

public interface BunqSerializer extends Wirespec.Serializer<String>, Wirespec.Deserializer<String>, DefaultParamSerialization {

}
