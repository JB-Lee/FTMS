package org.cnsl.ftms.utils

import androidx.lifecycle.MutableLiveData

class LiveArrayList<T> : MutableLiveData<ArrayList<T>>(), Iterable<T>, List<T> {

    init {
        value = ArrayList<T>()
    }

    override fun contains(element: T): Boolean {
        TODO("Not yet implemented")
    }

    override fun containsAll(elements: Collection<T>): Boolean = value!!.containsAll(elements)

    override fun get(index: Int): T = value!![index]

    override fun indexOf(element: T): Int = value!!.indexOf(element)

    override fun isEmpty(): Boolean = value!!.isEmpty()

    override fun lastIndexOf(element: T): Int = value!!.lastIndexOf(element)

    override fun listIterator(): ListIterator<T> = value!!.listIterator()

    override fun listIterator(index: Int): ListIterator<T> = value!!.listIterator(index)

    override fun subList(fromIndex: Int, toIndex: Int): List<T> = value!!.subList(fromIndex, toIndex)

    override fun iterator(): Iterator<T> = value!!.iterator()

    override val size: Int
        get() = value!!.size

    fun add(item: T) {
        val items = value
        items!!.add(item)
        value = items
    }

    fun addAll(list: List<T>) {
        val items = value
        items!!.addAll(list)
        value = items
    }

    fun clear(notify: Boolean) {
        val items = value
        items!!.clear()
        if (notify)
            value = items
    }

    fun remove(item: T) {
        val items = value
        items!!.remove(item)
        value = items
    }

    fun removeAt(index: Int) {
        val items = value
        items!!.removeAt(index)
        value = items
    }

    fun notifyChange() {
        val items = value
        value = items
    }

    operator fun set(idx: Int, v: T) {
        value!![idx] = v
    }


}