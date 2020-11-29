package org.cnsl.ftms.repository.remote.dao

import org.cnsl.ftms.net.AsyncClient
import org.cnsl.ftms.repository.remote.entities.FileItem

class FileItemDao(val host: String, val port: Int) {
    private val EOF = "\r\n\t\n\r".toByteArray()

    suspend fun createConnection(): AsyncClient {
        return AsyncClient.getInstance(host, port)
    }

    suspend fun getFileList(vararg file: FileItem) {


    }
}