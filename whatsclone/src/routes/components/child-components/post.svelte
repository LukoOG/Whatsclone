<script lang='ts'>
    import {activePost, Post} from '../../../context/store'
    import { formatDay } from '../../../context/logic';
    import { PUBLIC_BACKEND_URL } from '$env/static/public';

    export let profile
    export let posts

    let backend_url = PUBLIC_BACKEND_URL

    let profile_pic = posts[0].profile_pic
    let post_count = posts.length - 1
    const setStatus = () =>{
        $Post = posts
        $activePost = 0
    }
    // console.log(posts, post_count)

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

</script>

<div>
    <div on:keypress on:click={setStatus} class="flex items-center p-[15px] border border-b-[rgb(0,0,0,0.2)]">
        <div class="relative cursor-pointer w-[40px] h-[40px] rounded-[50%] overflow-hidden">
            <img class="absolute top-0 left-0 h-full w-full object-cover" src={"http://"+backend_url+profile_pic} alt="Profile">
        </div>
        <div class="ml-4">
            <h2 class="text-lg font-semibold">{posts[0].display}</h2>
            <p class="text-sm text-gray-600">{status_time(posts[post_count].time)}</p>
        </div>
    </div>
</div>