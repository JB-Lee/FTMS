package org.cnsl.ftms.repository.local.entities

import android.os.Parcelable
import androidx.databinding.BaseObservable
import androidx.databinding.Bindable
import androidx.room.Entity
import androidx.room.Ignore
import androidx.room.PrimaryKey
import kotlinx.android.parcel.Parcelize
import org.cnsl.ftms.BR

@Entity
@Parcelize
data class Client(
    @PrimaryKey var _id: String,
    var _pw: String,
    var _name: String
) : BaseObservable(), Parcelable {
    @Ignore
    var isAvailable: Boolean = false

    var id: String
        @Ignore @Bindable get() = _id
        set(value) {
            _id = value
            notifyPropertyChanged(BR.client)
        }

    var pw: String
        @Ignore @Bindable get() = _pw
        set(value) {
            _pw = value
            notifyPropertyChanged(BR.client)
        }

    var name: String
        @Ignore @Bindable get() = _name
        set(value) {
            _name = value
            notifyPropertyChanged(BR.client)
        }

}