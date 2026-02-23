// 1. Les données du graphique
const data = [{
    x: ['Girafes', 'Singes', 'Tigres', 'Lions', 'Éléphants'],
    y: [20, 14, 23, 18, 9],
    type: 'bar',
    marker: {
        color: '#3498db', // Une jolie couleur bleue
        opacity: 0.8
    }
}];

// 2. L'apparence du graphique (titre, axes, marges)
const layout = {
    title: 'Inventaire des animaux',
    font: { 
        family: 'Open Sans, sans-serif',
        size: 14 
    },
    xaxis: { title: 'Espèces' },
    yaxis: { title: 'Nombre d\'individus' },
    // margin permet d'éviter que le graphique ne colle trop aux bords
    margin: { t: 50, l: 50, r: 20, b: 50 } 
};

// 3. La configuration générale (barre d'outils, responsivité)
const config = {
    responsive: true, // Le graphique s'adapte à la taille de l'écran
    displayModeBar: true, // Affiche la barre d'outils au survol
    displaylogo: false, // Cache le petit logo Plotly dans la barre d'outils
    modeBarButtonsToRemove: ['lasso2d', 'select2d'] // Retire les outils de sélection inutiles
};

// 4. On demande à Plotly de créer le graphique dans la div "monGraphique"
Plotly.newPlot('monGraphique', data, layout, config);