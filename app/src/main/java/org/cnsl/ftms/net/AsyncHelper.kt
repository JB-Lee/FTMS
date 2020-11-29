package org.cnsl.ftms.net

import java.net.InetSocketAddress
import java.nio.ByteBuffer
import java.nio.channels.AsynchronousSocketChannel
import java.nio.channels.CompletionHandler
import java.util.concurrent.TimeUnit
import kotlin.coroutines.Continuation
import kotlin.coroutines.resume
import kotlin.coroutines.resumeWithException
import kotlin.coroutines.suspendCoroutine


class AsyncClient private constructor(private val host: String, private val port: Int) {

    private val socket by lazy {
        AsynchronousSocketChannel.open().apply {
            connect(InetSocketAddress(host, port))
                .get(5, TimeUnit.SECONDS)
        }
    }


    suspend fun recv(bufSize: Int): ByteArray {
        val buff = ByteBuffer.allocate(bufSize)
        socket.asyncRead(buff)

        println(buff.array().decodeToString())
        return buff.array()
    }

    suspend fun send(data: ByteArray) {
        val buff = ByteBuffer.wrap(data)
        socket.asyncWrite(buff)
    }

    fun close() {
        socket.close()
    }

    private suspend fun AsynchronousSocketChannel.asyncRead(buffer: ByteBuffer): Int {
        return suspendCoroutine { continuation ->
            this.read(buffer, continuation, CompletionHandlerImpl)
        }
    }

    private suspend fun AsynchronousSocketChannel.asyncWrite(buffer: ByteBuffer): Int {
        return suspendCoroutine { continuation ->
            this.write(buffer, continuation, CompletionHandlerImpl)
        }
    }

    object CompletionHandlerImpl : CompletionHandler<Int, Continuation<Int>> {
        override fun completed(result: Int, attachment: Continuation<Int>) {
            attachment.resume(result)
        }

        override fun failed(exc: Throwable, attachment: Continuation<Int>) {
            attachment.resumeWithException(exc)
        }
    }

    companion object {
        fun getInstance(host: String, port: Int): AsyncClient = AsyncClient(host, port)
    }

}