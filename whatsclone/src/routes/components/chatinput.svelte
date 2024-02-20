<script lang='ts'>
    import { send_message } from '../../context/django';
    import { User, DM, chatSocket, receiveSocket} from '../../context/store';
    import { createEventDispatcher } from 'svelte';

    import 'iconify-icon'
    import Emojis from './child-components/emojis.svelte';
    
    let message = ''
    let dispatch = createEventDispatcher()
    let message_field;
    let fileinput;
    let media: any = null;
    let showModal: boolean = false

    async function handleSubmit (event){
        if (event.key === 'Enter' && (media || event.target.value.trim()) && event.shiftKey == false){
            let formData = new FormData()
            media ? formData.append('media', media) : media = null
            message ? formData.append('message', message) : message = ''
            formData.append('email', $User.email)
            formData.append('participant', $DM.email)
            console.log(formData)
            let mess = await send_message(formData)
            showModal = false
            //console.log(mess)
            message = ''
            media = null
            if ($DM.Dm_id){
                $chatSocket.send(JSON.stringify({
                'user':$User.email,
                'message':mess
                }))   
            } else if($DM.Dm_id === null){
                console.log('sending to ', $receiveSocket.url)
                $receiveSocket.send(JSON.stringify({
                    'user':$User.email,
                    'message':mess
                }))
            }
        } else if(event){
            //console.log(event)
        }
    }

    let emoji = false
    const emojis = () =>{
        emoji = !emoji
    }

    const addEmoji = (event: any) =>{
        message += event.detail.emoji //update to add emoji after cursor
    }

    let img: any
    const submitFile = async(e)=>{
        console.log('uploading')
        let image = e.target.files[0]
        media = image
        let filereader = new FileReader()
        filereader.readAsDataURL(image)
        filereader.onloadend = (e: any)=>{
            dispatch('modal',{
            'image':e.target.result
        })
        img = e.target.result
        } 
        fileinput.value = ''
        showModal = true
    }
</script>

{#if showModal}
    <div class='absolute top-[50%] left-[50%] mt-[-50px] ml-[-50px]'>
        <p></p>
        <img class='' src={img} alt='cad'/>
    </div>
{/if}
<div class='chat-form'>
    <div class='relative flex w-full'>
        <button on:click={emojis} class='z-10'><iconify-icon icon="bxs:happy"></iconify-icon></button>
        <iconify-icon on:keydown on:click={fileinput.click()} icon="ion:attach"></iconify-icon>
        <input style='display:none' type='file' accept=".jpg, .jpeg, .png, .avif" on:change={(e)=>submitFile(e)} bind:this={fileinput}/>
        <input on:keydown={handleSubmit} type="text" bind:this={message_field} bind:value={message} placeholder="enter message"/>
        <!-- <textarea rows=1 class='textarea' on:keydown={handleSubmit} type="text" bind:this={message_field} bind:value={message} placeholder="enter message"/> -->
        <span on:keypress><iconify-icon on:keydown icon="gg:arrow-right-o"></iconify-icon></span> <!--use keydown event instead-->
    </div>
    {#if emoji}
        <div class='absolute top-0 mt-[-9rem] border-b border-b-black'>
            <Emojis on:emoji={addEmoji} on:blur={emojis}/>
        </div>    
    {/if}
</div>