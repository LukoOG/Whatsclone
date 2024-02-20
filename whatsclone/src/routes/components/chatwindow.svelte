<script lang='ts'>
  import Chatmessage from "./child-components/chatmessage.svelte";
  import {User, DM, chatSocket} from '../../context/store'
  import {seen_count, new_day} from '../../context/logic'
  import {formatDate, formatDay, formatYear, check_date} from '../../context/logic'

  import { afterUpdate, onDestroy, onMount } from "svelte";
	import { PUBLIC_BACKEND_URL } from "$env/static/public";
  export let image: any
   
    // console.log($DM)

    $: messages = $DM.messages
    $: online = $DM.online
    let showDatePopup = false

    $: console.log(seen_count(messages))
    //console.log($DM.messages[1].seen)


    let chatContainer: any;
    let backend_url = PUBLIC_BACKEND_URL
    function scrolltoBottom(){
        chatContainer.scrollTop = chatContainer.scrollHeight;
    }

    onMount(scrolltoBottom);
    afterUpdate(scrolltoBottom)
    onDestroy(()=>{image = ''})
    
    //date checking
    let today = new Date()
    $: last_login = new Date($DM.last_login)

    //displaying of date markers
    function shouldDisplayDateMarker(index: number) {
        if (index === 0) {
            return true;
        }

        const currentTimestamp = new Date(messages[index].date);
        const previousTimestamp = new Date(messages[index - 1].date);

        return !areDatesEqual(currentTimestamp, previousTimestamp);
    } //thanks GPT

    function areDatesEqual(dateA: any, dateB: any) {
        // Compare dates, ignoring time
        return (
            dateA.getFullYear() === dateB.getFullYear() &&
            dateA.getMonth() === dateB.getMonth() &&
            dateA.getDate() === dateB.getDate()
        );
    }
    
    const tcfest = (val: any) => {
      let today = new Date()
      let date = new Date(val)

      let factor = today - date
      return Math.floor(factor/(8.64e+7))
    }
    
</script>
<div class="header">
    <div class='imgText'><!--imgText-->
        <div class="relative w-[40px] h-[40px] rounded-[50%] overflow-hidden"><!--userImg-->
            <img src={"http://"+backend_url+$DM.profile_pic} class="absolute top-0 left-0 h-full w-full object-cover" alt={$User.email}/>
        </div>
        <h4><span>{$DM.name}</span></h4>
        {#if $DM.Dm_id}
          <h4><span>{online ? 'online' : 'last online ' + check_date(today, last_login)}</span></h4>
        {:else if $DM.Dm_id == null}
          <h4><span>{'date joined: ' + formatYear($DM.last_login)}</span></h4>
        {/if}
    </div>

    
    <ul class="flex">
        <li class="flex ml-[22px] text-[1.5rem] text-[#51585c]"><ion-icon name="search-outline"></ion-icon></li>
        <li class="flex ml-[22px] text-[1.5rem] text-[#51585c]"><ion-icon name="ellipsis-vertical"></ion-icon></li>
    </ul>
    
    <div>
      <h4 class='leading-[1.2em] font-[500] ml-[15px]'><span class='text-[0.75em] text-[#777]'>"{$DM.bio}"</span></h4>
    </div>
</div>

<!--chatbox-->
<div class="chat-box" bind:this={chatContainer}>
  
    {#each messages as message, i (i)}
      {#if shouldDisplayDateMarker(i)}
        <!-- Display date marker here -->
        <div class="date-marker">
            <div class='bg-[#f1f1f1] h-[24px] rounded-md w-[150px]'>
              <p class='text-center'>{new_day(message.date)}</p> 
            </div>
        </div>
      {/if}
      <Chatmessage {...message}/>
    {/each}

    {#if image}
      <img src={image} alt='not needed'/>
    {/if} 
</div>

<style>
/* Width and height for the scrollbar track */
::-webkit-scrollbar {
  width: 8px;
  height: 8px;
}

/* Background color of the scrollbar track */
::-webkit-scrollbar-track {
  background: #f1f1f1;
}

/* Styles for the scrollbar thumb */
::-webkit-scrollbar-thumb {
  background: #888;
  border-radius: 4px;
}

/* Styles when hovering over the scrollbar */
::-webkit-scrollbar-thumb:hover {
  background: #555;
}

/* Styles for the scrollbar corner */
::-webkit-scrollbar-corner {
  background: #f1f1f1;
}

.date-popup {
  position: absolute;
  top: 0;
  left: 50%;
  transform: translateX(-50%);
  background-color: rgba(0, 0, 0, 0.8);
  color: #fff;
  padding: 4px 8px;
  border-radius: 4px;
  z-index: 3;
}

.date-text {
  font-size: 14px;
  font-weight: bold;
}

/* Style the date marker as needed */
.date-marker {
  display: flex;
  position: sticky;
  justify-content: center;
  align-items: center;
  margin: 16px 0;
}
</style>