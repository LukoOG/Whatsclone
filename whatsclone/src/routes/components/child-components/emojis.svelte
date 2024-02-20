<script>
    import { createEventDispatcher } from "svelte";
    let dispatch = createEventDispatcher()

    let emojis = [
        '😂',
        '😀',
        '😃',
        '😄',
        '😆',
        '😅',
        '🤣',
        '🥲',
        '😇',
        '🙂',
        '🙃',
        '😉',
        '😍',
        '🥰',
        '😘',
        '😤',
        '😭',
        '😢',
    ]

    const sendEmoji = (emoji) => {
        dispatch('emoji',{
            emoji:emoji
        });
    }
</script>

<div class='h-60px flex w-full h-[60px]'>
    <div class=''>
        <div class='bg-white grid grid-cols-5 gap-2 p-2'>
            {#each emojis as emoji}
                <button on:click={()=>(sendEmoji(emoji))}>{emoji}</button>
            {/each}
        </div>
    </div>
</div>

<style>

</style>