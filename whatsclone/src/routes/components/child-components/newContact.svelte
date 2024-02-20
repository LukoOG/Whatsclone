<script lang='ts'>
    import {onDestroy} from 'svelte';    

    import { contacts, dm, DM, receiveSocket, chatSocket, newcontacts, User} from '../../../context/store';
	import { PUBLIC_BACKEND_URL } from '$env/static/public';
	import { get_user } from '../../../context/django';
    import { createEventDispatcher } from 'svelte';

    

    export let display_name: string
    export let email: string
    export let id: number
    export let phone: string
    export let profile_pic: string
    export let bio: string
    export let date_joined: string
    export let online: boolean
    // let _silence = last_login && online //to shut it up

    const dispatch = createEventDispatcher()
    const init = () => {
        dispatch('init', {
            'detail':email
        })
    }

    const updateContact = (chat: any)=>{
        contacts.update((contacts)=>{
            contacts.unshift(chat)
            //console.log(email, contacts, 'update')
            return contacts
        })     
    }

    const updatenewContact = ()=>{
        newcontacts.update((newcontacts)=>{
            const updatedContacts = newcontacts
            let _id = updatedContacts.findIndex(chat=>chat.id == id) //let _id because it will clash if I used let id
            updatedContacts.splice(_id, 1)
            console.log('removed', _id, $newcontacts)
            return newcontacts
        })
    }

    // let date: string
    // let ready = false
    let backend_url = PUBLIC_BACKEND_URL

    const setDM = () => {
        let DM_contact = new dm([], id, null, display_name ? display_name : phone, bio, email, profile_pic, date_joined, online)
        $DM = DM_contact
        $receiveSocket = receivesocket
        //console.log($receiveSocket, 'set')
        $chatSocket = ''
    }

    //receive socket to send and make new dm
    let receivesocket = new WebSocket(`ws://${backend_url}/new/${id}`)

    $: receivesocket.onmessage = async (e)=>{
        let data = JSON.parse(e.data)
        console.log('received', data)
        if (data.user == $User.email){ //cuz multiple people could be connected to this socket at once
            if(data.type == 'new_message'){
                let new_contact = await get_user(email, data.message.date)
                $DM.last_login = new_contact.last_login
                $DM.Dm_id = new_contact.Dm_id
                $DM.index = new_contact.index
                $DM.messages = [...$DM.messages, data.message]
                $receiveSocket = ''
                $chatSocket = new WebSocket(`ws://${backend_url}/dm/${$DM.Dm_id}`)
                console.log($User.email, $contacts)
                updateContact(new_contact)
                updatenewContact()
                init()
            }
        }
    }
    onDestroy(()=>{receivesocket.close(); console.log('closed')}) //because the connection persisted after changing accounts. Causing the double receive
</script>
<div on:keypress on:click={setDM} class="hover:bg-[#f5f5f5] cursor-pointer relative flex items-center p-[15px] border border-b-[rgb(0,0,0,0.2)]">
    <!--chat box child-template-->
    <div class="imgbx">
        <img src={"http://"+backend_url+profile_pic} class="absolute top-0 left-0 h-full w-full object-cover" alt={bio}/>
    </div>

    <div class="details">
        <div class="flex justify-between ">
            <h4 class="text-[1.1em] font-[600px] text-[#111]">{display_name ? display_name : phone}</h4>
            <p class="text-[0.75em] text-[#aaa]">{phone}</p>
        </div>
    </div>
</div>
