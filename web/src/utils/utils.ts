export function generateRandomString(length = 16) {
    const characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
    let result = '';
    for (let i = 0; i < length; i++) {
        result += characters.charAt(Math.floor(Math.random() * characters.length));
    }
    return result;
}

export function randomColorQuadrant2() {
    const center = { r: 135, g: 65, b: 65 }

    // Quadrante 2 → R > 135 e G > 65
    const r = Math.floor(135 + Math.random() * (255 - 135))
    const g = Math.floor(65 + Math.random() * (255 - 65))
    const b = Math.floor(Math.random() * 200) // azul opcional, controla saturação

    return `rgb(${r}, ${g}, ${b})`
}
