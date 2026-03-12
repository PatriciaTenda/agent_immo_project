

class Interactions{
    constructor(){
         this.interact_container = document.querySelector(".interact")
    }

    question_pipeline(){
        let user_prompt = document.querySelector("textarea").value
        this.add_question("user", user_prompt)
        document.querySelector("textarea").value = ""
        try{
            // fonction patricia
            let bad_response = true  // a enlever une fois fonction ajoutée
            setTimeout(()=>{
                if(bad_response == true){
                    console.log('une erreur s\'est produite')
                    let agent_response = "Une erreur s'est produite."
                    this.add_question("agent", agent_response)
                } 
                    }, 2000)
            
        }
        catch{
            
        }
        
        
        
        
        
        }
    get_response(){
        ErrorEvent
    }
    add_question(type, data){
        let question = document.createElement("div")
        question.className = "question"
        question.innerHTML = `
                                <div class="${type}">
                                    <p class="data">${data}</p>
                                </div>
                            `
        this.interact_container.appendChild(question)
        
    }
    

}


const interact_ = new Interactions()