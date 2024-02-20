<script lang='ts'>
	import { Post, activePost } from "../../context/store";
    import { formatDay } from "../../context/logic";
    import { PUBLIC_BACKEND_URL } from "$env/static/public";
    import { onMount } from "svelte";

    import { Spinner } from "flowbite-svelte";
	import Statusinput from "./child-components/statusinput.svelte";

    let backend_url = PUBLIC_BACKEND_URL

    const today = new Date()

    let fileinput: any
    let message_field
    let message=''

    const status_time = (time: string)=>{
        let options = {hour:'numeric', minute:'numeric', hour12:true}
        let Time = new Date(time)
        if(formatDay(today) == formatDay(Time)){
            return 'today '+Time.toLocaleString('en-us', options)
        } else{
            return 'yesterday '+Time.toLocaleString('en-us',options)
        }
    }
    
    const filetype = (file)=>{
        if(file.endswith === '3'){
            return 'video'
        }
        else{
            return 'img'
        }
    }

    // let fetching: boolean = false

    // const fetchpost = (post: any)=>{
    //     let url = `http://${backend_url}${post}`
    //     if(url){
    //         fetching = true
    //     }
    //     return url
    // }

    // let url: any;
    // $: if($Post){
    //     url = fetchpost($Post[0].media)
    // }

function nextPost() {
  activePost.update(value => (value === $Post.length - 1 ? 0 : value + 1));
}

function prevPost() {
  activePost.update(value => (value === 0 ? $Post.length - 1 : value - 1));
}
</script>

{#if $Post}
<div class='h-full relative z-10 flex items-center flex-col justify-around'>
    <div class="header absolute top-0">
            <div class="imgText">
                <div class="relative w-[40px] h-[40px] rounded-[50%] overflow-hidden">
                    <img src={"http://"+backend_url+$Post[0].profile_pic} class="absolute top-0 left-0 h-full w-full object-cover" alt={$Post.profile}/>
                </div>
                <h4 class='text-[#000000]'><span>{status_time($Post[$activePost].time)}</span></h4>
            </div>
        </div>
    {#each $Post as post, index (index)}
        <div class='{index === $activePost ? 'active' : 'inactive'} mt-[calc(60px+10px)] h-[calc(80%-60px)]'>
            {#if post.media}
                <img class='h-[calc(100%-20px)] rounded-xl  z-20' src={"http://"+backend_url+post.media} alt={post.caption}/>
            {/if}
            <p class='{post.media ? '' : 'txt-post'} text-center font-bold rounded-xl z-20'>{post.caption}</p>
        </div>    
        
    {/each}
  
    <!-- to style and position as left and right arrows -->
    <button on:click={prevPost}>Previous</button>
    <button on:click={nextPost}>Next</button>
    </div>

{:else}
    <Statusinput />
{/if}

<style>
    /* Hide inactive posts */
    .inactive {
      display: none;
    }
  
    /* Add styles for active post */
    .active {
      display: block;
      /* Additional styles for the active post */
    }

    .txt-post{
        color: blue;
        font-size: 2.25rem;
    }
</style>