package org.cnsl.ftms.repository.remote.dao

import org.cnsl.ftms.repository.remote.entities.FileItem

interface FileItemDao {

    suspend fun getFileList(from: String, path: String, requester: String): List<FileItem>

    suspend fun add(
        from: String,
        pathFrom: String,
        to: String,
        pathTo: String,
        requester: String,
        item: FileItem
    ): Boolean

    suspend fun getRootPath(from: String, requester: String): String

    suspend fun getUUID(): String

    suspend fun ping(from: String): Boolean

}