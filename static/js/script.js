document.addEventListener(
    "DOMContentLoaded",
    function () {

        const search =
            document.getElementById(
                "userSearch"
            );

        if(search){

            search.addEventListener(
                "keyup",
                function(){

                    let value =
                        this.value.toLowerCase();

                    document
                    .querySelectorAll(
                        "#userTable tr"
                    )
                    .forEach(row=>{

                        row.style.display =
                            row.textContent
                            .toLowerCase()
                            .includes(value)

                            ? ""

                            : "none";
                    });
                }
            );
        }
    }
);

const counters =
document.querySelectorAll(".counter");

counters.forEach(counter => {

    const updateCounter = () => {

        const target =
            +counter.getAttribute(
                "data-target"
            );

        const current =
            +counter.innerText;

        const increment =
            Math.ceil(target / 50);

        if(current < target){

            counter.innerText =
                current + increment;

            setTimeout(
                updateCounter,
                30
            );

        }else{

            counter.innerText =
                target;
        }
    };

    updateCounter();

});