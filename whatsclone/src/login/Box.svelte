<script lang='ts'>
    import Register from './register.svelte'
    import Login from './login.svelte';

    import { get_token} from '../context/django';
    import { login_box } from '../context/store';

    import {fly, fade} from 'svelte/transition'
    
    let email: string

</script>

{#if $login_box}
    <section in:fly={{y:100, duration:400}} out:fade={{duration:0}}>
        <Login />
    </section>
    
{:else}
<section in:fly={{y:100, duration:400}} out:fade={{duration:0}}>
        <Register />
    </section>    
{/if}
