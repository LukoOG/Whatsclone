<script lang='ts'>
    import {onDestroy, onMount} from 'svelte';    

    import { dm, contacts, User, DM, chatSocket, receiveSocket} from '../../../context/store';
    import {formatDate, formatDay, formatYear} from '../../../context/logic'
	import { PUBLIC_BACKEND_URL } from '$env/static/public';

    import { fly } from 'svelte/transition';
	import { get_last_login, offline } from '../../../context/django';
    
    export let display_name: string
    export let email: string
    export let Dm_id: number
    export let id: number
    export let phone: string
    export let profile_pic: string
    export let bio: string
    export let index: string
    export let last_login: string
    export let online: boolean
    let silence = index

    const loadMessages = async ()=>{
        let res = await fetch(
            `http://${backend_url}/api/message`, {
                'method':'POST',
                'headers':{
                    'Content-Type':'application/json'
                },
                'body': JSON.stringify({user:$User.email, participant:email})
            }
        )
        let data = await res.json()
        setMessages(data)
        return data
    }
	
	let user_id = $User.user_id

    let sender: string
    let message: string
    let no_messages: number
    let date: string
    let ready = false
    let backend_url = PUBLIC_BACKEND_URL

    $: setMessages = (data) =>{
        no_messages = data.length -1
        message = data[no_messages].message
        date = data[no_messages].date
        sender = data[no_messages].sender
        ready = true
   }

    let messages: any
    const getMessages = async ()=>{
        return await loadMessages()
    }
    
    const setDM = async () =>{
        let DM_contact = new dm(messages, id, Dm_id, display_name ? display_name : phone, bio, email, profile_pic, last_login, online)
        $DM = DM_contact
        $chatSocket = chatsocket
        $receiveSocket = ''
        console.log('set',email)
    }

    //update chatlist functions
    //try remembering the updating index alternative
    const updateContact = (index: string)=>{
        contacts.update((contacts)=>{
            const updatedContacts = contacts
            let id = updatedContacts.findIndex(chat=>chat.Dm_id == Dm_id)
            const chat = updatedContacts[id]
            updatedContacts.splice(id, 1)
            updatedContacts.unshift(chat)
            return updatedContacts 
        })     
    }
    
    //by now the messages variable is accessible
    (async () => {
        messages = await getMessages()
    })()

    //chatsocket code
    let url = `ws://${backend_url}/dm/${Dm_id}`
    const chatsocket = new WebSocket(url)
    
    $: chatsocket.onmessage = async function(e){
        let data = JSON.parse(e.data)
       // console.log(data)

        if(data.type === 'dm_message'){
            no_messages+= 1
            message = data.message.message
            date = data.message.date
            sender = data.message.sender
            messages = [...messages, data.message] //updating the actual message variable so it still remains
            if($DM.Dm_id == Dm_id){
                $DM.messages = [...$DM.messages, data.message] //updates the chatwindow if this contact is the one active
            }
            updateContact(date)
        }else if(data.type === 'connection established'){
            chatsocket.send(JSON.stringify({
                'user':$User.email,
                'message':true //telling this contact that we are online
            }))
        } else if(data.type == 'online_offline'){
            if (data.user !== $User.email){ //it also sends to the logged in user, so have to check for that
                online = data.message //it's the online status...I named it this way cuz of the conflict in the socket and the normal message
                if(online == false){
                    let res = await get_last_login(data.user)
                    last_login = res.last_login
                }
                if($DM.Dm_id == Dm_id){
                    $DM.online = online
                    if(online == false){
                        let res = await get_last_login(data.user)
                        $DM.last_login = res.last_login
                    }                 
                }
            }
        }
    }  
    //online_offline. To inform others who are online about the user's status

    window.addEventListener('beforeunload', function (e) {
        offline(_email)
        chatsocket.send(JSON.stringify({
                'user':_email,
                'message':false
            }))
        chatsocket.close();
        });

    onMount(()=>{loadMessages})
    
    let _email = $User.email
    onDestroy(()=>{ //offline() is run at chatlist logout, so no need to rerun
        chatsocket.send(JSON.stringify({
                'user':_email,
                'message':false
            }))
        chatsocket.close();
        })


    let today = new Date()
    const check_date = (today:any, _date:any) => {
        let date = new Date(_date)
      if(formatDay(today) == formatDay(date)){
        return formatDate(date)
      }else{
        return (formatYear(date)) //yes yes. Will still work on this piece of trash //9/8...hang on....just add year options na //lol, the fact that it was an easy fix(21/9-time of recording)
      }
    }
</script>
{#if ready}
<div on:keypress on:click={setDM} class="anim hover:bg-[#f5f5f5] cursor-pointer relative flex items-center p-[15px] border border-b-[rgb(0,0,0,0.2)]">
    <!--chat box child-template-->
    <div class="imgbx">
        <img src={"http://"+backend_url+profile_pic} class="absolute top-0 left-0 h-full w-full object-cover" alt={bio}/>
    </div>

    <div class="details">
        <div class="flex justify-between ">
            <h4 class="text-[1.1em] font-[600px] text-[#111]">{display_name ? display_name : phone}</h4>
            <p class="text-[0.75em] text-[#aaa]">{check_date(today, date)}</p>
        </div>
        <!--message_p-->
        <div class="flex items-center justify-between"> <!---to replace pic with an icon-->
            <p class="text-[#aaa] line-clamp-1 text-[0.9em] overflow-ellipsis">{sender == user_id ? 'You: ' : ''}{message ? message : 'pic'}</p>
            <b class="bg-[#05d755] text-[0.75em] text-[#fff] min-w-[20px] h-[20px] rounded-[50%] flex justify-center items-center">{no_messages + 1}</b>
        </div>
    </div>
</div>
{:else}
<div in:fly={{y:-10, duration:300}} on:keypress on:click={setDM} class="hover:bg-[#f5f5f5] cursor-pointer relative flex items-center p-[15px] border border-b-[rgb(0,0,0,0.2)]">
    <!--chat box child-template-->
    <div class="imgbx">
        <img src={"http://"+backend_url+profile_pic} class="absolute top-0 left-0 h-full w-full object-cover" alt={bio}/>
    </div>

    <div class="details">
        <div class="flex justify-between ">
            <h4 class="text-[1.1em] font-[600px] text-[#111]">{display_name ? display_name : phone}</h4>
            <p class="text-[0.75em] text-[#aaa]"></p>
        </div>
        <!--message_p-->
        <div class="flex items-center justify-between">
            <p class="text-[#aaa] line-clamp-1 text-[0.9em] overflow-ellipsis">...Loading</p>
        </div>
    </div>
</div>
{/if}

<style>
    .anim{
        transition: 2s ease;
    }
</style>