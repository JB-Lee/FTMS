package org.cnsl.ftms.repository.remote.entities

data class FileItem(
    val name: String,
    val size: Int,
    val isFile: Boolean,
    val last_modified: Int
)