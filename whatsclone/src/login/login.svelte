<script lang='ts'>
    import jwt_decode from 'jwt-decode';

    import { User, login_box, token, ready } from "../context/store";
	import { browser } from '$app/environment';
	import { PUBLIC_BACKEND_URL } from '$env/static/public';



    let email: string
    let phone: string
    let backend_url = PUBLIC_BACKEND_URL
 
    const handleSubmit = async () => {
        ready.update((val)=>(!val))
        let phone_no = '+234'+phone
        const res = await fetch(
        `http://${backend_url}/api/token`, {
            'method':'POST',
            'headers':
                {'Content-Type':'application/json'},
            'body':
                JSON.stringify({email:email, password:phone_no})
            }
        )

        let data = await res.json()
        if (res.ok){
            token.subscribe((value) => {browser && localStorage.setItem('tokens', JSON.stringify(data))})
            $User = jwt_decode(data.access)
            ready.update((val)=>(!val))
        }
        else if(res.ok == false){
            alert('invalid login credentials')
            ready.update((val)=>(!val))
        }
    }

    const toggle_login_box = () => {
        login_box.update((value)=>(!value))
    }
</script>

<div class='w-[400px] relative items-center mx-auto my-0]'>
    <div class="form_box">
        <h1>Login</h1>
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
            >
            <input type='submit'>
        </form>
        <button on:click={toggle_login_box}>Click here to register</button>
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
        height: calc(100vh-70px);
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