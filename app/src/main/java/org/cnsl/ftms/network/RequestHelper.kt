package org.cnsl.ftms.network

import org.bson.BSONObject
import org.bson.BasicBSONDecoder
import org.bson.BasicBSONEncoder
import org.bson.BasicBSONObject
import java.net.Socket

class RequestHelper(private val host: String, private val port: Int) {
    fun request(
        method: Any,
        session: String?,
        params: Map<String, *>,
        onSuccess: (BSONObject) -> Unit,
        onFail: ((BSONObject) -> Unit)?
    ): RequestHelper {
        val bson = BasicBSONObject(
            mapOf(
                "method" to method,
                "session" to session,
                "params" to params
            )
        )
        val encoder = BasicBSONEncoder()
        val decoder = BasicBSONDecoder()

        val conn = Socket(host, port)

        val reader = conn.getInputStream()
        val writer = conn.getOutputStream()

        writer.write(encoder.encode(bson))

        val result = decoder.readObject(reader.readBytes())

        if (result.containsField("result"))
            onSuccess(result)
        else if (result.containsField("error"))
            if (onFail != null) {
                onFail(result)
            }

        conn.close()
        return this
    }

}