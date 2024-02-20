//all the functions regarding sending data to django backend
import { PUBLIC_BACKEND_URL } from "$env/static/public"
let backend_url = PUBLIC_BACKEND_URL
export const login = async () =>{
    let res = fetch(
        `http://${backend_url}/api/token`, {
            'method':'POST',
            'headers':{
                'Content-Type':'application/json'
            },
            'body':
                JSON.stringify({})
        }
    )
}

//register
export const register = async (email:string, phone:string) =>{
    let res = fetch(
        `http://${backend_url}/api/register/`,{
            'method':'POST',
            'headers':{
                'Content-Type':'application/json'
            },
            'body':
                JSON.stringify({email:email, password:phone, phone:phone})            
        }
    )
    const data = (await res).json()
    return data
}

export const otp_verification = async (email: string, otp: string) =>{
    let res = fetch(
        `http://${backend_url}/api/verify_otp/`,{
            'method':'POST',
            'headers':{
                'Content-Type':'application/json'
            },
            'body':
                JSON.stringify({email:email, otp: otp})            
        }
    )
    const data = (await res).json()
    return data 
}
//
export const get_token = async (email: string, phone: string) =>{
    let res = await fetch(
        `http://${backend_url}/api/token`, {
            'method':'POST',
            'headers':
                {'Content-Type':'application/json'},
            'body':
                JSON.stringify({email:email, password:phone})
        }
    )
    const data = (await res).json()
    return data
}

export const refresh_token = async (token: string) =>{
    let res = fetch(
        `http://${backend_url}/api/token/refresh`,{
            'method':'POST',
            'headers':{
                'Content-Type':'application/json'
            },
            'body':
                JSON.stringify({refresh:token})            
        }
    )
    let data = (await res).json()
    return data

}

// export const send_message = async (email: string, participant: string, message:any) => {
//     let res = fetch(
//         `http://${backend_url}/api/create`, {
//             'method':'POST',
//             'headers':{
//                 'Content-Type':'application/json'
//             },
//             'body':JSON.stringify({
//                 email:email, participant:participant, message:message
//             })
//         }
//     )
//     const data = (await res).json()
//     return data
// }

export const send_message = async (message:any) => {
    let res = fetch(
        `http://${backend_url}/api/create`, {
            'method':'POST',
            'body':message
        }
    )
    const data = (await res).json()
    return data
}

export const get_user = async (email: string, message: any) => {
    let res = fetch(`http://${backend_url}/api/get_user`, {
            'method':'POST',
            'headers':{
                'Content-Type':'application/json'
            },
            'body':JSON.stringify({
                user:email, message:message
            })
    })
    let data = (await res).json()
    return data
}

export const online = async (email: string) => {
    let res = fetch(
        `http://${backend_url}/api/online`, {
            'method':'POST',
            'headers':{
                'Content-Type':'application/json'
            },
            'body':JSON.stringify({
                email:email
            })
        }
    )
    let data = (await res).json()
    return data
}

export const offline = async(email: string)=>{
    let res = fetch(
        `http://${backend_url}/api/offline`, {
            'method':'POST',
            'headers':{
                'Content-Type':'application/json'
            },
            'body':JSON.stringify({
                email:email
            })
        }
    )
    let data = (await res).json()
    return data
}

export const get_last_login = async (email: string)=>{
    let res = fetch(
        `http://${backend_url}/api/last_login`, {
            'method':'POST',
            'headers':{
                'Content-Type':'application/json'
            },
            'body':JSON.stringify({
                email:email
            })
        }
    )
    let data = (await res).json()
    return data
}

export const uploadFile = async(file: any) => {
    let res = fetch(
        `http://${backend_url}/api/update_profile-pic`, {
            'method':'POST',
            // 'headers':{
            //     'Content-Type':'multipart/form-data'
            // },
            'body':file
        }
    )
    let data = (await res).json()
    return data
}

export const uploadInfo = async(email:string, info: any, endpoint: string) => {
    let res = fetch(
        `http://${backend_url}/api/${endpoint}`, {
            'method':'POST',
            'headers':{
                'Content-Type':'application/json'
            },
            'body':JSON.stringify({
                email:email, info:info
            })
        }
    )
    let data = (await res).json()
    return data
} //this is used for both name and about. The difference is the endpoint
//to improve UX. No need for a return. It'll just save in the database. The frontend will update the User from the form

//reading this on 10/8 - I must be one smart sexy devil :rofl:

export const create_post = async (file:any) =>{
    let res = fetch(
        `http://${backend_url}/api/createpost`,{
            'method':'POST',
            'body': file
        }
    )
    let data = (await res).json()
    return data
}

//