<script lang='ts'>
    import {User, token, ready} from '../context/store'
    import { offline } from '../context/django';
    import { PUBLIC_BACKEND_URL } from '$env/static/public';
    import '../app.css'
	import Box from '../login/Box.svelte';
	import { onMount, onDestroy } from 'svelte';
    import {Spinner} from 'flowbite-svelte'
	import jwt_decode from 'jwt-decode';

    let backend_url = PUBLIC_BACKEND_URL

    
    onMount(()=>{
        let obj: any = localStorage.getItem('tokens')
        let tokens: any = JSON.parse(obj)
        $token = tokens
        if($token){
            $User = jwt_decode($token.access)
        }
        ready.update((val)=>(!val))
    })

</script>

{#if $ready}
    {#if $User}
        <div class="container">
            <slot>

            </slot>
        </div>
    {:else if !$User}
        <Box/>
    {/if}
{:else}
        <div>
            <Spinner size={'12'} color={'green'}/>
            <p>...Loading</p>
        </div>
{/if}


<style lang="postcss">
    :global(body){
        display: flex;
        justify-content: center;
        align-items: center;
        min-height: 100vh;
        background: linear-gradient(#f8f8f8 4%, #f8f8f8 12px, #d9d9d9 100%, #d9dbd9 0px); /**color to be done later **/
    }

    :global(*){
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }
</style> 