<script lang='ts'>
    import 'iconify-icon'
    import Chatlist from './chatlist.svelte';   
    
    import { User, token } from '../../context/store';
    import { createEventDispatcher } from 'svelte';

    import { PUBLIC_BACKEND_URL } from '$env/static/public';
    import { browser } from '$app/environment';
	import { Spinner } from 'flowbite-svelte';
	import { get_token, uploadFile, uploadInfo } from '../../context/django';

    let backend_url = PUBLIC_BACKEND_URL
    let dispatch = createEventDispatcher()

    $: img = $User.profile_pic
    //let img = "http://"+backend_url+'/static/account/images/julianakarupe@gmail.com/carpe.jpg'
    let fileinput: any
    let name_input: any
    let about_input: any
    let uploading: boolean = false

    let name: string = $User.display_name
    let bio: string = $User.bio
    if($User.display){
        name = $User.display
    }

    const submitFile = async(e: any) => {
        console.log('uploading')
        uploading = true
        let image = e.target.files[0]
        let formData = new FormData()
        formData.append('profile_pic', image)
        formData.append('email',$User.email)
        console.log(formData)
        let res = await uploadFile(formData) //to do after configuring backend......DONE
        console.log(res)
        // let fileReader = new FileReader()
        // fileReader.readAsDataURL(image)
        // fileReader.onloadend = (e: any) => {
        //     img = e.target.result
        //     // let res = await uploadFile()
        //     //img = '/static/account/images/julianakarupe@gmail.com/carpe.jpg' //just testing...it works
        //     //console.log(e)
        // } legacy code lol. Works but client side specific
        if(res.status === 200){
            $User.profile_pic = res.profile_pic
            let _token = await get_token($User.email, $User.phone)
            token.subscribe((value) => {browser && localStorage.setItem('tokens', JSON.stringify(_token))})      
        } //gots save it in the client too
        uploading = false
        console.log(uploading)
    }

    const changecomponent = () =>{
        dispatch('component', {
            'component':Chatlist
        })
    }

    import jwt_decode from 'jwt-decode';
	import { fade } from 'svelte/transition';
    const handleSubmit = async(e: any) =>{
        if(e.keyCode === 13){
            switch (e.target.id) {
                case 'name':
                    $User.display = name;
            
                case 'bio':
                    $User.bio = bio;
            }
            let res = await uploadInfo($User.email, e.target.value, e.target.name)
            let _token = await get_token($User.email, $User.phone)
            if(res.status == 200){ //just to wait for the database to save the change
                token.subscribe((value) => {browser && localStorage.setItem('tokens', JSON.stringify(_token))}) //gots save the change on client too
                console.log(jwt_decode(_token.access))
            }
        } //was able to shorten the code with switch and some backend configing
    }
</script>
<div in:fade={{duration:500}} out:fade={{duration:200}}>
<div class='header'>
    <div class='cursor-pointer text-[1.5rem]'>
        <iconify-icon on:keydown on:click={changecomponent} icon='gg:arrow-left-o'></iconify-icon>
        <!-- <p on:keypress on:click={changecomponent}>as</p> -->
    </div>
    <h3>Update your Profile</h3>
</div>

<div class='profile-img'>
    <div class='form'>
        <img class='' src={uploading ? '' : "http://"+backend_url+img} alt={$User.display_name} width="100" height="100"/>
        {#if uploading}
            <div class='absolute top-[116px]'><Spinner size={'12'} color={'green'}/></div> <!--116 as per half the image height-->
        {/if}
        <div class='relative items-center flex flex-col p-2'>
            <iconify-icon class='cursor-pointer' on:keydown on:click={()=>{fileinput.click()}} icon='ph:camera-bold'></iconify-icon>
            <p class='cursor-pointer text-center' on:keydown on:click={()=>{fileinput.click()}}>Click here to update your profile pic</p>
        </div>
        <input style='display:none' type='file' accept=".jpg, .jpeg, .png, .avif, .webp" on:change={(e)=>submitFile(e)} bind:this={fileinput}/>
    </div>
</div>

<div class='profile-info'>
    <div class='w-full flex flex-col items-center'>
        <input id='name' name='update_username' on:keydown={handleSubmit} bind:value={name} bind:this={name_input} on:focus={()=>{name_input.value = ''}} on:blur={()=>{name_input.value = name}} class='outline-none w-[80%] border-b border-black text-[#a1a1a1]' placeholder="enter a name"/>
    </div>

    <div class='w-full flex flex-col items-center'>
        <input id='bio' name='update_userbio' on:keydown={handleSubmit} bind:value={bio} bind:this={about_input} on:focus={()=>{about_input.value = ''}} on:blur={()=>{about_input.value = bio}} class='outline-none w-[80%] border-b border-black text-[#a1a1a1]' placeholder="enter your bio"/>
    </div>
</div>
</div>

<style>
    *{
        /* border: solid 1px black; */
        box-sizing: border-box;
    }

    .profile-img{
        width: 100%;
        display: flex;
        flex-direction: column;
        margin: 0 auto;
        position: relative;
        justify-content: space-around;
        /* box-sizing: border-box */
    }

    .profile-img .form{
        margin: 1.5rem auto;
        padding: 2px;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: space-between;
    }

    .profile-img .form img{
        position: relative;
        width: 230px;
        height: 230px;
        border-radius: 50%;
        overflow: hidden;
    }

    .profile-info{
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        margin: 10px 0
    }

    .profile-info div{
        margin: 10px 0;
        
    }
</style>