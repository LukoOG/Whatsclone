<script lang="ts">
    import { User, ready } from "../../context/store";

    let otp: string
    export let email: string
    export let otp_verification: Function

    const handleSubmit = async () => {
        const data = await otp_verification(email, otp)
        if(data.status == 400){
            alert(data.message)
            console.log(data)
        } else if(data.status == 200){
            alert(data.message)
            $User = data.data
            console.log($User)
        }
    }
</script>

<div class='w-[400px] relative items-center mx-auto my-0]'>
    <div class="form_box">
        <h1>Enter OTP</h1>
        <form on:submit|preventDefault={handleSubmit}>
            <p>enter your OTP for verification</p>
            <input type='text' required bind:value={otp}>
            <input type='submit'>
        </form>
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