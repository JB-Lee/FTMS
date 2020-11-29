package org.cnsl.ftms.net

import org.bson.BSONObject
import org.bson.BasicBSONDecoder
import org.bson.BasicBSONEncoder
import org.bson.BasicBSONObject
import java.net.Socket

class RequestHelper(private val host: String, private val port: Int) {

    companion object {
        val EOF = "\r\n\t\n\r".toByteArray()
    }

    fun request(
        method: Any,
        session: String?,
        params: Map<String, *>?,
        onSuccess: (BSONObject) -> Unit,
        onFail: ((BSONObject) -> Unit)?
    ): RequestHelper {
        val protocol = mutableMapOf("method" to method)

        if (session != null)
            protocol["session"] = session

        if (params != null)
            protocol["params"] = params

        val bson = BasicBSONObject(protocol)
        val encoder = BasicBSONEncoder()
        val decoder = BasicBSONDecoder()

        val conn = Socket(host, port)

        val reader = conn.getInputStream()
        val writer = conn.getOutputStream()

        writer.write(encoder.encode(bson) + EOF)

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

    suspend fun asyncRequest(
        method: Any,
        session: String?,
        params: Map<String, *>?
    ): BSONObject {
        val protocol = mutableMapOf("method" to method)

        val client = AsyncClient.getInstance(host, port)

        if (session != null)
            protocol["session"] = session

        if (params != null)
            protocol["params"] = params

        val bson = BasicBSONObject(protocol)
        val encoder = BasicBSONEncoder()
        val decoder = BasicBSONDecoder()

        client.send(encoder.encode(bson) + EOF)
        val result = client.recv(1024)

        val bsonResult = decoder.readObject(result)

        client.close()

        return bsonResult
    }

}
