package org.cnsl.ftms.repository.remote.dao

import org.cnsl.ftms.net.RequestHelper
import org.cnsl.ftms.repository.remote.entities.FileItem

class FileItemDaoImpl(private val host: String, private val port: Int) : FileItemDao {

    private var _count = 0

    private val count: String
        get() = (_count++).toString()

    override suspend fun getFileList(from: String, path: String, requester: String): List<FileItem> {
        RequestHelper(host, port).apply {
            val sess_id = requester + count
            val res = asyncRequest(
                method = "get_dir",
                session = sess_id,
                params = mapOf(
                    "header" to mapOf(
                        "from" to from,
                        "requester" to sess_id
                    ),
                    "path" to path
                ),
            ).get("result") as Map<*, *>

            val list = ArrayList<FileItem>()

            (res["dirs"] as List<*>).forEach {
                it as Map<*, *>
                list.add(
                    FileItem(
                        it["name"] as String, it["size"] as Int, it["is_file"] as Boolean,
                        it["last_modified"] as Int
                    )
                )
            }
            return list
        }

    }

    override suspend fun add(
        from: String,
        pathFrom: String,
        to: String,
        pathTo: String,
        requester: String,
        item: FileItem
    ): Boolean {
        RequestHelper(host, port).apply {
            val sess_id = requester + count
            val res = asyncRequest(
                method = "sendFile",
                session = sess_id,
                params = mapOf(
                    "header" to mapOf(
                        "from" to from,
                        "to" to to,
                        "requester" to sess_id
                    ),
                    "src" to mapOf(
                        "path" to pathFrom,
                        "file_name" to item.name
                    ),
                    "dst" to mapOf(
                        "path" to pathTo,
                        "file_name" to item.name
                    )
                ),
            ).get("result") as Map<*, *>

            return res["is_success"] as Boolean

        }


    }

    override suspend fun getRootPath(from: String, requester: String): String {
        RequestHelper(host, port).apply {
            val sess_id = requester + count
            val res = asyncRequest(
                method = "get_root",
                session = sess_id,
                params = mapOf(
                    "header" to mapOf(
                        "from" to from,
                        "requester" to sess_id
                    )
                ),
            ).get("result") as Map<*, *>

            return res["cwd"] as String
        }
    }

    override suspend fun getUUID(): String {
        RequestHelper(host, port).apply {
            val res = asyncRequest(
                method = "getUuid",
                session = null,
                params = null,
            ).get("result") as Map<*, *>
            return res["uuid"] as String
        }
    }

    override suspend fun ping(from: String): Boolean {
        RequestHelper(host, port).apply {
            val res = asyncRequest(
                method = "ping",
                session = null,
                params = mapOf(
                    "client" to from
                ),
            ).get("result") as Map<*, *>

            return (res["is_success"] as Boolean)
        }
    }
}