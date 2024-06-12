const fs = require('fs');
const path = './medicamentos.json';

function loadMedicamentos() {
    if (fs.existsSync(path)) {
        const data = fs.readFileSync(path, 'utf8');
        return JSON.parse(data);
    } else {
        return [];
    }
}

function saveMedicamentos(medicamentos) {
    fs.writeFileSync(path, JSON.stringify(medicamentos, null, 2), 'utf8');
}

function agregarMedicamento(nombre, frecuencia) {
    const medicamentos = loadMedicamentos();
    medicamentos.push({ nombre, frecuencia, historial: [] });
    saveMedicamentos(medicamentos);
    console.log(`Medicamento ${nombre} agregado con frecuencia de ${frecuencia} horas.`);
}

function registrarToma(nombre) {
    const medicamentos = loadMedicamentos();
    const medicamento = medicamentos.find(med => med.nombre === nombre);
    if (medicamento) {
        const ahora = new Date().toISOString();
        medicamento.historial.push(ahora);
        saveMedicamentos(medicamentos);
        console.log(`Registro de toma para ${nombre} a las ${ahora}.`);
    } else {
        console.log(`Medicamento ${nombre} no encontrado.`);
    }
}

function verHistorial(nombre) {
    const medicamentos = loadMedicamentos();
    const medicamento = medicamentos.find(med => med.nombre === nombre);
    if (medicamento) {
        console.log(`Historial de tomas para ${nombre}:`);
        medicamento.historial.forEach((toma, index) => {
            console.log(`${index + 1}. ${toma}`);
        });
    } else {
        console.log(`Medicamento ${nombre} no encontrado.`);
    }
}

// Ejemplos de uso:
agregarMedicamento('Paracetamol', 8);
registrarToma('Paracetamol');
verHistorial('Paracetamol');
