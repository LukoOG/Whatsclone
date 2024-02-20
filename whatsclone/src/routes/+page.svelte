<script lang='ts'>
    import Chatlist from "./components/chatlist.svelte";
	import Chatwindow from "./components/chatwindow.svelte";
    import Chatinput from "./components/chatinput.svelte";
    import Status from "./components/status.svelte";
    import Statuswindow from "./components/statuswindow.svelte";
    import Mediamodal from "./components/child-components/mediamodal.svelte";

    import { DM, User, contacts, status, statuslist, user_receiveSocket, user_status, Post} from "../context/store";
    import { offline, online } from "../context/django";
    import { fade } from "svelte/transition";

    import { onMount, onDestroy } from 'svelte'
	import { PUBLIC_BACKEND_URL } from "$env/static/public";
	import { Modal } from "flowbite-svelte";
	

    let backend_url = PUBLIC_BACKEND_URL

    const sortByTime = (a, b) => {
        const timeA = a.index
        const timeB = b.index
        return new Date(timeB) - new Date(timeA)

    }


    onMount(async () => {
        online($User.email) //set online in backend
        fetch(
            `http://${backend_url}/api/contact`, {
                'method':'POST',
                'headers':{
                    'Content-Type':'application/json'
                },
                'body':JSON.stringify({user:$User.email})
            }
        ).then(response => response.json())
        .then(data =>{
            data.sort(sortByTime)
            contacts.set(data)
        })

        fetch(
            `http://${backend_url}/api/status`,{
                'method':'POST',
                'headers':{
                    'Content-Type':'application/json'
                },
                'body':JSON.stringify({user:$User.email})

            }
        ).then(response => response.json())
        .then(data=>{
            data.sort(sortByTime)
            statuslist.set(data)
        })

        fetch(
            `http://${backend_url}/api/user_status`,{
                'method':'POST',
                'headers':{
                    'Content-Type':'application/json'
                },
                'body':JSON.stringify({user:$User.email})
            }
        ).then(response=>response.json())
        .then(data=>{
            user_status.set(data)
        })
    })

    const removeWindow = (event) =>{
        if(event.keyCode === 27){
            $DM ? $DM = null : $Post = null
        }
    }

    let image: any;
    const setImage = (event: any)=>{
        image = event.detail.image
    }

    $user_receiveSocket = new WebSocket(`ws://${backend_url}/new/${$User.user_id}`)
    let email = $User.email
    onDestroy(()=>{offline(email)})

    let component = Chatlist //thank you rich harrison

    const changeComponent = (event: any) =>{
        component = event.detail.component
    }

    $: if($status){component = Status}
    $: if(!$status){component = Chatlist}
</script>

<svelte:window on:keydown={removeWindow}/>

<!--z-index to place newlist over contact list-->
<div transition:fade class="left-container">
    <svelte:component on:component={changeComponent} this={component} />
</div>

<div class="right-container">
    {#if $DM}
        <Chatwindow {image}/>
        <Chatinput/>
    {:else if $status}
        <Statuswindow />
    {:else}
        <div class='chat-box'>
            <div class='flex items-center flex-row justify-center font-black'>
                Thanks for choosing this Knock off Whatsapp built by a sadistic black teenager
            </div>
        </div>
    {/if}
</div>

<style lang="postcss">
   .right-container::before{
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: url(favicon.png); /*customization option to be done*/
    opacity: 0.9;
   }
</style>