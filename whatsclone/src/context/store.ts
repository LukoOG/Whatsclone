import { writable, derived } from "svelte/store";

//global variable to manage state and components
export const login_box = writable(true)

export const User = writable(null)

export const token = writable(null)

export const ready = writable(false)

export const status = writable(false)

//the dm store
export class dm {
    messages;
    id;
    name;
    bio;
    constructor(messages:Array<Object>, id: number, Dm_id: number, name: string, bio: string, email:string, profile_pic:string, last_login:string, online:boolean){
        this.messages = messages
        this.id = id
        this.Dm_id = Dm_id
        this.name = name
        this.bio = bio
        this.email = email
        this.profile_pic = profile_pic
        this.last_login = last_login
        this.online = online
    }
    format(){
        return this.name
    }
}

export class post{
    constructor(profile_pic, post, caption, profile, time){
        this.profile_pic = profile_pic
        this.post = post
        this.caption = caption
        this.profile = profile
        this.time = time
    }
    format(){
        return this.caption
    }
}

export let contacts = writable([])
export let newcontacts = writable([])
export let DM = writable(null)
export let statuslist = writable([])
export let user_status = writable([])
export let Post = writable(null)
export let activePost = writable(0);
//time for date checking

//global chatsocket for the selected dm
export let chatSocket = writable('')
export let receiveSocket = writable('') //this will always be on, what others connect to initialize a new dm before going to the other one
export let user_receiveSocket = writable('') //for the user