const cheerio = require('cheerio');
const ref_data = require('./api/data/ref.json');

const mesesNumeros = {
  Enero: 1, 
  Febrero: 2, 
  Marzo: 3, 
  Abril: 4, 
  Mayo: 5, 
  Junio: 6,
  Julio: 7, 
  Agosto: 8, 
  Septiembre: 9, 
  Octubre: 10, 
  Noviembre: 11, 
  Diciembre: 12,
}

function interpretarTipoFeriado(tipo) {
  const tipoMap = {
    immovable: 'inamovible',
    transferable: 'trasladable',
    bridge: 'puente',
  }
  return tipoMap[tipo] || 'otro'
}

async function extraerFeriados(año) {
  const url = `https://www.lanacion.com.ar/feriados/${año}`;
  const response = await fetch(url);
  const html = await response.text();
  const $ = cheerio.load(html);

  const calendarios = $('div.holidays-card-calendar');
  const feriados = calendarios.map((_, div) => {
    const mes = $(div).find('h3.com-text').text();
    const diasFeriados = $(div).find('ul.holidays-list li');

    const feriadosMes = diasFeriados.map((_, li) => {
      const dia = $(li).find('span').text();
      const tipo = $(li).find('span').attr('class');
      const nombre = $(li).find('h4.com-text').text();

      return {
        fecha: new Date(año, mesesNumeros[mes] - 1, Number(dia)).toISOString().split('T')[0],
        tipo: interpretarTipoFeriado(tipo.replace(/[^a-zA-Z0-9]/g, '')),
        nombre,
        info: ref_data[nombre] ? ref_data[nombre].url : '',
      };
    }).get();

    return feriadosMes;
  }).get();

  return feriados.flat();
}

/* Para exportar manualmente
const fs = require('fs');

async function exportarjson(año) {
  const feriados = await extraerFeriados(año);
  const data = JSON.stringify(feriados, null, 2);
  fs.writeFileSync(`./api/data/${año}.json`, data);
}

exportarjson(2025);
*/