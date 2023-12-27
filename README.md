# SITL FOR SERVER ON UBUNTU 64-bit OS


## 1. Adding a new Mavlink Message
You can create new mavlink message, for that you need to create entry in common.xml. Message id will be last id + 1.
```
<message id="12921" name="NEW_MESSAGE_NAME">
      <description>DESCRIBE THE FIELD</description>
      <field type="uint8_t" name="FIELD_NAME"></field>
    </message>
```

* In ```GCS_MAVLink/GCS.h``` create a virtual method to use it appropriate, for example:-
  ```C
  // Handle new message
    virtual void handle_new_message(const mavlink_new_message_name_t &packet) { }
  ```
and a method to decode respective message from mavlink chunk
```C
void handle_new_message(const mavlink_message_t &packet);
```
* In ```GCS_MAVLink/GCS_Common.cpp``` define definition of encoding, for example:-

```C
void GCS_MAVLINK::handle_new_message(const mavlink_message_t &msg)
{
    mavlink_new_message_t m;
    mavlink_new_message_decode(&msg, &m);
    handle_new_message(m);
}
```
and call it is switch case based on message ID:-
```C
// Handle new auth handle
    case MAVLINK_MSG_NEW_MESSAGE:
        handle_new_message(msg);
        break;
```
* For Python ```pymavlink```, genrate using mavgen.py and paste the new ardupilotmega.py to respective location where pymavlink was installed using:-
```bash
cp ardupilotmega.py $HOME/.local/lib/python3.8/site-packages/pymavlink/dialects/v20/ardupilotmega.py
```
