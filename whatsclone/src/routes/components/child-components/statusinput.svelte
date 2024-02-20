<script lang='ts'>
    import { create_post } from "../../../context/django";
    import { User, user_status } from '../../../context/store'
    import { PUBLIC_BACKEND_URL } from "$env/static/public";
    import { Spinner } from "flowbite-svelte";
    import Emojis from "./emojis.svelte";

    let backend_url = PUBLIC_BACKEND_URL

    let message = ''
    let media: any = null
    let fileinput: any
    
    async function handleSubmit (event){
        if (event.key === 'Enter' && (media || event.target.value.trim()) && event.shiftKey == false){
            let formData = new FormData()
            media ? formData.append('media', media) : media = null
            message ? formData.append('caption', message) : message = ''
            formData.append('email', $User.email)
            console.log(formData)
            let mess = await create_post(formData)
            //showModal = false
            console.log(mess)
            $user_status = [...$user_status, mess]

            message = ''
            media, img = null
            if(event){
            //console.log(event)
            }
        }
    }

    let emoji = false
    const emojis = () =>{
        emoji = !emoji
        console.log(emoji)
    }

    const addEmoji = (event: any) =>{
        message += event.detail.emoji //update to add emoji after cursor
    }

    let img: any;
    let uploading: boolean = false
    const submitFile = async(e)=>{
        console.log('uploading', uploading)
        uploading = true
        let image = e.target.files[0]
        media = image
        let filereader = new FileReader()
        filereader.readAsDataURL(image)
        filereader.onloadend = (e: any)=>{
            img = e.target.result
        } 
        // fileinput.value = ''
        // //showModal = true
        uploading = false
        console.log('uploading',uploading)
    }
</script>

<div>
    <div class='chat-box flex flex-col items-center h-[500px]'>
        <p class='mb-[10px] text-center font-[20px]'>View a status or make yours</p>
        <img class='border-none' src={uploading ? '' : img} alt={$User.display_name} width="350" height="350"/>
        {#if uploading}
            <div class='absolute top-[250px]'><Spinner size={'12'} color={'green'}/></div>
        {/if}

        <div class='absolute mt-8 bottom-3 flex items-center flex-row justify-center'>
            <button on:click={emojis} class='z-10'><iconify-icon icon="bxs:happy"></iconify-icon></button>
            <iconify-icon class='text-[28px]' on:keydown on:click={fileinput.click()} icon="ion:attach"></iconify-icon>
            <input style='display:none' type='file' accept=".jpg, .jpeg, .png, .avif, .webp" on:change={(e)=>submitFile(e)} bind:this={fileinput}/>
            <input on:keydown={handleSubmit} type="text" bind:value={message} placeholder="enter message"/>
        </div>
        {#if emoji}
        <div class='absolute bottom-[calc(200px-12px-32px)] mt-[-9rem] border-b border-b-black'>
            <Emojis on:emoji={addEmoji} on:blur={emojis}/>
        </div>    
    {/if}
    </div>
</div>

<style>

</style>