<script lang='ts'>
    import { register } from "../context/django";
    import { otp_verification } from "../context/django";

	import Otp from "./components/otp.svelte";
	import RegisterForm from "./components/register_form.svelte";

    let otp: boolean = false
    let email: string

    const alertOtp = (event: any) =>{
        alert(event.detail.message)
        email = event.detail.email
        otp = !otp
    }
</script>

{#if otp}
    <Otp {email} {otp_verification}/>
{:else}
    <RegisterForm on:otp={alertOtp} {register} />
{/if}