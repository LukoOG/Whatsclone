<script lang='ts'>
    import { status, statuslist, User, Post, user_status, activePost } from '../../context/store';
    import Posts from './child-components/post.svelte';
    import { formatDay } from '../../context/logic';
    import { fade } from 'svelte/transition';

    import { PUBLIC_BACKEND_URL } from '$env/static/public';

    let backend_url = PUBLIC_BACKEND_URL

    let time;
    $: last_post = $user_status.length - 1
    $: if ($user_status){time = $user_status[last_post].time} else{time = null} 

    
    const close = ()=>{
        $Post = null
        $status = false
    }

    let today = new Date()
    const status_time = (time: string)=>{
        let options = {hour:'numeric', minute:'numeric', hour12:true}
        let Time = new Date(time)
        if(formatDay(today) == formatDay(Time)){
            return 'today '+Time.toLocaleString('en-us', options)
        } else{
            return 'yesterday '+Time.toLocaleString('en-us',options)
        }
    }

    const setStatus = () =>{
        $Post = $user_status
        $activePost = 0
    }

    //Posts, because the component and store name will clash
    console.log($statuslist)

    
</script>

<div class='status-box' in:fade={{duration: 300}} out:fade={{duration:300}}>
    <div class="header">
        <div on:keypress on:click={setStatus} class="flex items-center">
            <div class="relative cursor-pointer w-[40px] h-[40px] rounded-[50%] overflow-hidden">
                <img class="absolute top-0 left-0 h-full w-full object-cover" src={"http://"+backend_url+$User.profile_pic} alt="Profile">
            </div>
            <div class="ml-4">
                <h2 class="text-lg font-semibold">{$User.display}</h2>
                <p class="text-sm text-gray-600">{status_time(time)}</p>
            </div>
        </div>
        <p on:keydown class='cursor-pointer' on:click={close}><iconify-icon icon="mingcute:close-fill"></iconify-icon></p> 
    </div>
    {#each $statuslist as {profile, posts}, i (i)}
        <Posts {profile} {posts}/>
    {/each}
</div>