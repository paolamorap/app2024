document.getElementById('updateTopologyButton').addEventListener('click', function() {
    updateTopology();
});

function updateTopology() {
    const script = document.createElement('script');
    script.src = '/js/topology.js';
    script.onload = () => {
        console.log('Topología actualizada con éxito.');
        // Aquí puedes llamar a cualquier función que necesite reutilizar los datos actualizados
        initializeTopology(topologyData);
    };
    script.onerror = () => {
        console.error('Error al cargar los datos de topología.');
    };
    // Remueve el script antiguo y añade el nuevo
    const oldScript = document.querySelector('script[src="/js/topology.js"]');
    if (oldScript) {
        document.body.removeChild(oldScript);
    }
    document.body.appendChild(script);
}
