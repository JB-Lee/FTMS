package org.cnsl.ftms.fileview

data class FileItem(
    val isFile: Boolean,
    val name: String,
    val size: Int,
    val last_modified: Long
)