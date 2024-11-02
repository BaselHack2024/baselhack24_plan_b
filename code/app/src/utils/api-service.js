const IP = '192.168.20.250'

export const createProcessId = async () => {
    const rawResponse = await fetch(`http://${IP}:8000/api/create-process`, {
        method: 'POST',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
        body: null
    });
    const content = await rawResponse.json();
    return content
}

export const startProcess = async (processId) => {
    const rawResponse = await fetch(`http://${IP}:8000/api/initiate-process`, {
        method: 'POST',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ process_id: processId })
    });
    const content = await rawResponse.json();
    return content
}

export const uploadPicturesToProcess = async (images, processId) => {
    const url = `http://${IP}:8000/api/add_image/${processId}`;
    const uploadResult = [];
    for (const image of images) {
        const formData = new FormData();

        formData.append('file', new Blob([image], { type: 'image/jpeg' }), image.name);

        try {
            const response = await fetch(url, {
                method: 'POST',
                headers: {
                    'accept': 'application/json',
                },
                body: formData
            });

            if (!response.ok) {
                throw new Error(`Upload failed: ${response.statusText}`);
            }

            const result = await response.json();
            console.log("Upload successful:", result);
            uploadResult.push({
                state: 'success',
                image: image
            });
        } catch (error) {
            console.error("Error uploading image:", error);
            uploadResult.push({
                state: 'error',
                image: image
            });
        }
    }

    return uploadResult;
}


export const checkResult = async (processId) => {
    const rawResponse = await fetch(`http://${IP}:8000/api/result/${processId}`, {
        method: 'GET',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }
    });
    const content = await rawResponse.json();
    return content
}