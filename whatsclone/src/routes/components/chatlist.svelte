  <script lang='ts'>

    import 'iconify-icon'
    import { Dropdown, DropdownItem, Button, Chevron } from 'flowbite-svelte'


    import Contact from "./child-components/contact.svelte";
    import Newcontact from './child-components/newContact.svelte'
    import Userform from './userform.svelte';
    
	import { User, contacts, newcontacts, token, DM, user_receiveSocket, chatSocket, receiveSocket, status} from '../../context/store';
    import { get_user, offline } from '../../context/django';
    import { browser } from '$app/environment';    
	import { PUBLIC_BACKEND_URL } from '$env/static/public';
    import { onMount, onDestroy, createEventDispatcher} from 'svelte';
	import { fade, fly } from 'svelte/transition';
    
    let backend_url = PUBLIC_BACKEND_URL
    let dispatch = createEventDispatcher()
    let chatlist: boolean = false

    let search: string
    const logout = async () =>{
        offline($User.email)
        $DM = null
        token.subscribe((val) => {browser && localStorage.removeItem('tokens')})
        User.update((val)=>{val = null})
        $contacts = []
        $newcontacts = []
        $chatSocket = ''
        $receiveSocket = ''
        $user_receiveSocket = ''
    }

    const changecomponent = () =>{
        dispatch('component', {
            'component':Userform
        })
    }
//for newchats

onMount(async () => {
        const res = await fetch(
            `http://${backend_url}/api/newcontact`, {
                'method':'POST',
                'headers':{
                    'Content-Type':'application/json'
                },
                'body':JSON.stringify({user:$User.email})
            }
        )
        let data = await res.json()
        newcontacts.set(data)
    })

//for user receive socket
    const updateContact = (chat: any)=>{
            contacts.update((contacts)=>{
                contacts.unshift(chat)
                return contacts
            })     
        }
    const updatenewContact = (id: number)=>{
    newcontacts.update((newcontacts)=>{
        const updatedContacts = newcontacts
        let _id = updatedContacts.findIndex(chat=>chat.id == id) //let _id because it will clash if I used let id
        updatedContacts.splice(_id, 1)
        console.log('removed', _id)
        return newcontacts
    })
    }
 
$: $user_receiveSocket.onmessage = async function (e){
    let data = JSON.parse(e.data)
    if(data.type == 'new_message'){
        let new_contact = await get_user(data.user, data.message.date)
        updateContact(new_contact)
        updatenewContact(new_contact.id)
        console.log('received message from', new_contact.email)
    }
}
    let name = $User.display ? $User.display : $User.email
    let verified = $User.is_verified
</script>

<!--header-->
<div in:fade={{duration:500}} out:fade={{duration:100}}>
{#if $User}
    <div class="header">
        <div class="relative cursor-pointer w-[40px] h-[40px] rounded-[50%] overflow-hidden">
            <img on:keydown on:click={changecomponent} src={"http://"+backend_url+$User.profile_pic} class="absolute top-0 left-0 h-full w-full object-cover" alt='user'/>
        </div>

        <p class='text-[1rem] text-[#777]'>{name}</p>
        <ul class="flex"> 
            <li on:keydown on:click={()=>{$status = true; $DM = null}} class="flex cursor-pointer ml-[22px] text-[1.5rem] text-[#51585c]"><iconify-icon icon='streamline:interface-edit-select-area-circle-dash-select-area-object-work'></iconify-icon></li>
            <li on:keydown on:click={()=>(chatlist = !chatlist)} class="flex cursor-pointer ml-[22px] text-[1.5rem] text-[#51585c]"><iconify-icon icon='ph:chat-bold'></iconify-icon></li>
            <div class='flex cursor-pointer my-0 mx-0 text-[1.5rem] text-[#51585c] z-10'>
                <Button><Chevron><li class="flex cursor-pointer m-0 text-[1.5rem] text-[#51585c]"><iconify-icon icon='pajamas:ellipsis-v'></iconify-icon></li></Chevron></Button>
                <Dropdown>
                    <DropdownItem on:click={logout}>Logout</DropdownItem>
                </Dropdown>
            </div>
            
        </ul>
    </div>

    <!--search bar-->
    <div class="search-chat">
        <div>
            <input type="text" bind:value={search} placeholder="search">
            <ion-icon name="search-outline"></ion-icon>
        </div>
    </div>
    <!---chat-list-->
    <!---Issue found-->
    <!---problem is that, the newcontact component isnt destroyed after the if condition. Hence why the sockets receive-->
    <!---multiple times. Need to find a way to fix that, as using the ternary operator messes up the logout-->
    {#if verified}
        <div class='chat-list {chatlist? 'hidden': ''} '>
                    {#each $contacts as contact (contact.index)}
                        <Contact {...contact} on:click/>
                    {:else}
                        <div class="flex items-center justify-between">
                            <p class="text-[#999] text-center text-[1.4em]"><span class='text-[1.1em]'>what's up</span><br>click on the <iconify-icon icon='ph:chat-bold'></iconify-icon><span>to get started</span></p>
                        </div>
                    {/each}
                <!--key transition re-renders. So it gives the same issue as the one in updateContacts in contact.svelte-->
        </div>

        <div class='{chatlist? '': 'hidden'}'>
            <div>
                <h4>New chats</h4>
            </div>
            <div transition:fade class='chat-list z-10'>
                {#each $newcontacts as contact (contact.id)}
                    <Newcontact {...contact} on:init={()=>(chatlist = !chatlist)}/>
                {/each}
            </div>
        </div>
    {:else}
        <p>Click here to verify your account</p>
    {/if}
{/if}
</div>