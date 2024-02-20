<script lang='ts'>
	import { User } from "../../../context/store";
    import { PUBLIC_BACKEND_URL } from "$env/static/public";
    let backend_url = PUBLIC_BACKEND_URL

    export let message: string
    export let date: string
    export let profile: string
    export let sender: number
    export let profile_pic: string
    export let media: any
    export let seen: boolean
    
    const toggle_class = (user: string) =>{
        if(user === $User.email){
            return 'user_message'
        }else{
            return '_message'
        }
    }

    const formatDate = (dateString: string)=>{
        const date = new Date(dateString);
        const options = { hour: 'numeric', minute: 'numeric', hour12: true };
        const formattedDate = date.toLocaleString('en-us', options);
        return formattedDate;
    }
</script>

<div class=''>
    <div class="message {toggle_class(profile)}">
        <p class='' >
            {#if media}
                <img class='h-[25rem] w-[25rem] rounded-xl' src={"http://"+backend_url+media} alt={message}/>
            {/if}
            {message}<br><span>{formatDate(date)}</span>
        </p>
    </div>
</div>

<style lang='postcss'>
    .user_message p::before{
        content: '';
        position: absolute;
        top: 0;
        right: -12px;
        width: 20px;
        height: 20px;
        background: linear-gradient(135deg, #dcf8c6 0%, #dcf8c6 50%, transparent 50%, transparent)
    }

    ._message p::before{
        content: '';
        position: absolute;
        top: 0;
        left: -12px;
        width: 20px;
        height: 20px;
        background: linear-gradient(225deg, #fff 0%, #fff 50%, transparent 50%, transparent)
    }

    .caption{
        margin: 0 auto
    }
</style>