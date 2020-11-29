package org.cnsl.ftms.utils

import androidx.databinding.BaseObservable
import androidx.databinding.Observable
import androidx.lifecycle.MutableLiveData

class CustomMutableLiveData<T : BaseObservable>(value: T) : MutableLiveData<T>(value) {

    private val callback = object : Observable.OnPropertyChangedCallback() {
        override fun onPropertyChanged(sender: Observable?, propertyId: Int) {
            value.let { setValue(it) }
        }

    }

    override fun setValue(value: T) {
        super.setValue(value)
        value.addOnPropertyChangedCallback(callback)
    }


}