//will migrate some functions here

export const day = (date: any) =>{
    let today = new Date()
    let _date = new Date(date)
    if (today.toDateString() == _date.toDateString()){
        // console.log('return today')
        return 'today'
    } else{
        // console.log('return date', today, _date)
        return date
    }
} //decided to optimize. Or had to lol

export const new_day = (val: any) => {
    let today = new Date()
    today.setHours(0)
    today.setMinutes(0)
    today.setSeconds(0) //so that "today" remains consistent
    today.setMilliseconds(0) //with this I now get perfect whole numbers

    let date = new Date(val)
    let _date = date //for calculation. Have to remove the hours, minutes and seconds for better precision
    _date.setHours(0)
    _date.setMinutes(0)
    _date.setSeconds(0)
    _date.setMilliseconds(0)
    
    let factor = today - _date
    // let value = Math.round(factor/(8.64e+7))
    let value = factor/8.64e+7 //no need to round again since milliseconds are gone
    switch (value){
        case 0:
            return 'today'
        case 1:
            return 'yesterday'
        case 2:
        case 3:
        case 4:
        case 5:
        case 6:
            return date.toLocaleDateString('en-us', {weekday: 'long'})
        default:
            return date.toLocaleDateString()
    }

  } //my best case of optimization "pats self on the back"

  //pains me to have to redo this. Cuz using milliseconds isn't that effecitve

  //ok just overpaniced. Able to figure it out, logic remains the same, but had to make some changes
  //to account for occurences like the diff between 11:59pm and 12am. SO set the hours of the previous day to 12am
  //so it always has a constant difference

export const seen_count = (  messages:any ) =>{
    let val = { messages }
    let j = 0
    for(let i =0; i<messages.length; i++){
        if(messages[i].seen === false){
            j++
        }
    }
    return j
}


//formate date functions
export const formatDate = (dateString: string)=>{
    const date = new Date(dateString);
    const options = { hour: 'numeric', minute: 'numeric', hour12: true };
    const formattedDate = date.toLocaleString('en-us', options);
    return formattedDate;
}

export const formatDay = (dateString: string)=>{
    const date = new Date(dateString);
    const options = { month: 'numeric', day: 'numeric' };
    const formattedDate = date.toLocaleString('en-us', options);
    return formattedDate;
}

export const formatYear = (dateString: string)=>{
    const date = new Date(dateString);
    const options = { month: 'numeric', day: 'numeric', year:'numeric'};
    const formattedDate = date.toLocaleString('en-us', options);
    return formattedDate;
}

export const check_date = (today:any, date:any) => {
    // console.log(date)
    if(formatDay(today) == formatDay(date)){
      return formatDate(date)
    }else{
      return ('on ' + formatYear(date))
    }
  }