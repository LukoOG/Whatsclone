<script lang="ts">
    import { login_box, ready } from "../../context/store";
    import { createEventDispatcher } from "svelte";
    import {Spinner} from "flowbite-svelte"

    let email: string
    let phone: string
    export let register: Function

    const dispatch = createEventDispatcher();
    const otp = () =>{
        dispatch('otp', {
            'message':'Check your email for the otp code',
            'email':email
        })
    }
    const handleSubmit = async () => {
        submit = false
        let phone_no = '+234'+phone
        console.log(email, phone_no)
        const data = await register(email, phone_no)
        console.log(data)
        if (data.status == 400){
            for(let i in data.error){
                alert(data.error[i])
            }
            submit = true
        }
        else if (data.status == 200){
            otp()
        }
    }

    const toggle_login_box = () => {
        login_box.update((value)=>(!value))
    }
    let submit: boolean = true
</script>

<div class='relative items-center mx-auto my-0]'>
    <div class="form_box">
        <h1>Register here</h1>
        <form on:submit|preventDefault={handleSubmit}>
            <p>Enter Your Phone Number</p>
            <div class='flex justify-between items-center relative p-1'>
                <label class='text-white text-lg mx-1 border-r p-2 border-r-1 border-r-white' for='phone_no'>+234</label>
                <div class='relative p-3'>
                    <input id='phone_no' required type='text' bind:value={phone} >
                </div>
            </div>
            <p>Enter Your Email</p>
            <input type='text' required bind:value={email}
            pattern='[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]$'>
                {#if submit}
                    <input type='submit'>
                {:else}
                    <div class='text-center'>
                        <Spinner size={'12'} color={'green'}/>
                    </div>
                {/if}
        </form>
        <button disabled={!submit} on:click={toggle_login_box}>Click here to login</button>
    </div>
</div>

<style lang='postcss'>
    h1{
        font-weight: bold;
        font-size: 32px;
        color: white;
        text-align: center;
    }
    .form_box{
        position: absolute;
        left: 50%;
        top: 50%;
        transform: translate(-50%, -50%);
        box-shadow: 10px, 1px, 3px, 4px;
        background-color: rgb(102, 223, 207);
        width: 320px;
        padding: 70px 30px;
        box-sizing: border-box;
        border-radius: 25px;
    }

    .form_box input{
        height: 40px;
        width: 100%;
        margin-bottom: 20px;
        color: white;
    }

    .form_box input[type='text']{
     
        background-color: rgb(102, 223, 207);
        outline: none;
        border: none;
        border-bottom: 1px solid white;
    }

    .form_box input[type='submit']{
        cursor: pointer;
        border: none;
        border-radius: 12.5px;
        background-color: black;
    }
</style>