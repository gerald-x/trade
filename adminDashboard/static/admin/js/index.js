document.addEventListener("DOMContentLoaded", () => {
    const updateTableData = ()=>{
        fetch(`${window.location.protocol}//${window.location.host}/dashboard/admin/user/all`)
            .then(res => res.json())
            .then(data => {
                const tbody = document.querySelector('tbody');
                const htmlRows = data.map((row, index) => {
                    const mainObject = row[0];
                    console.log(mainObject);
                    if (mainObject.hasOwnProperty("current_value")) {
                        console.log(mainObject.user__first_name)
                        return ` 
                    <tr>
                    <td>${index + 1}</td>
                    <td>${mainObject?.user__first_name}</td>
                    <td>${mainObject?.user__last_name}</td>
                    <td>${mainObject?.user__email}</td>
                    <td>${mainObject?.user__initial_deposit}</td>
                    <td class="date">${new Intl.DateTimeFormat('en-US', {
                            month: 'long',
                            day: 'numeric',
                            year: 'numeric',
                            hour: 'numeric',
                            minute: 'numeric',
                            hour12: true
                        }).format(new Date(mainObject?.time))}</td>
                    <td>${mainObject?.current_value}</td>                
                    `
                    } else {
                        return ` 
                    <tr>
                    <td>${index + 1}</td>
                    <td>${mainObject?.first_name}</td>
                    <td>${mainObject?.last_name}</td>
                    <td>${mainObject?.email}</td>
                    <td>${mainObject?.initial_deposit}</td>
                    <td class="date">Not Started</td>
                    <td>${mainObject?.initial_deposit}</td>                
                    `
                    }
                })
                tbody.innerHTML = htmlRows.join('')
            })
        .catch(error=>console.log("Error updating table"))
    }
    
    updateTableData();

    setInterval(updateTableData, 10000);
})