document.addEventListener('DOMContentLoaded', function() {

    (function (nx) {
        var showLabels = false; // Controla la visibilidad de las etiquetas
        // Define CustomLinkClass
        nx.define('CustomLinkClass', nx.graphic.Topology.Link, {
            properties: {
                sourcelabel: null,
                targetlabel: null,
                index: {
                    value: 0 // Valor predeterminado para el índice
                }
            },
            view: function(view) {
                view.content.push({
                    name: 'source',
                    type: 'nx.graphic.Text',
                    props: {
                        'class': 'sourcelabel',
                        'alignment-baseline': 'text-after-edge',
                        'text-anchor': 'start'
                    }
                }, {
                    name: 'target',
                    type: 'nx.graphic.Text',
                    props: {
                        'class': 'targetlabel',
                        'alignment-baseline': 'text-after-edge',
                        'text-anchor': 'end'
                    }
                });
                return view;
            },


            methods: {
                update: function() {
                    this.inherited();
                    var el, point, line = this.line();
                    var angle = line.angle();
                    var stageScale = this.stageScale();
                    var index = this.model().get('index');
                    // Determina el color basado en si el puerto esta bloqueado
                    var colorSourcelabel = this.model().get('port_bloks') === true ? 'red' : 'black';
                    var colorTargetlabel = this.model().get('port_blokt') === true ? 'red' : 'black';

                    // Ajustamos la separación de las etiquetas para cada índice de enlace
                    var labelSeparation = 10; // Este valor determina la separación entre las etiquetas de los enlaces
                    var indexOffset = (index-1) * labelSeparation;

                    // Desplazamiento en Y basado en el índice para evitar superposición
                    var deltaY = indexOffset;
                    var deltaX = indexOffset; 
                    
                    line = line.pad(20 * stageScale, 20 * stageScale);

                    if (this.sourcelabel()) {
                        el = this.view('source');
                        point = line.start;
                        el.set('x', point.x );
                        el.set('y', point.y );
                        el.set('text', this.sourcelabel());
                        el.set('transform', 'rotate(' + angle + ' ' + (point.x - deltaX) + ',' + (point.y - deltaY) + ')');
                        el.setStyle('font-size', 10 * stageScale);
                        el.setStyle('fill', colorSourcelabel); // Establece el color de la fuente aquí
                        this.view('source').visible(showLabels); 
                    }
                    if (this.targetlabel()) {
                        el = this.view('target');
                        point = line.end;
                        el.set('x', point.x );
                        el.set('y', point.y );
                        el.set('text', this.targetlabel());
                        el.set('transform', 'rotate(' + angle + ' ' + (point.x - deltaX) + ',' + (point.y - deltaY) + ')');
                        el.setStyle('font-size', 10 * stageScale);
                        el.setStyle('fill', colorTargetlabel); // Establece el color de la fuente aquí
                        this.view('target').visible(showLabels);
                    }
                }
            }             
        });

        nx.define('CustomNodeTooltip', nx.ui.Component, {
            properties: {
                node: {},
                topology: {}
            },
            view: {
                content: [{
                    tag: 'div',
                    content: [{
                        tag: 'h5',
                        content: [{
                            tag: 'a',
                            content: '{#node.model.name}',
                            props: {"href": "{#node.model.dcimDeviceLink}"}
                        }],
                        props: {
                            "style": "border-bottom: dotted 1px; font-size:90%; word-wrap:normal; color:#003688"
                        }
                    }, {
                        tag: 'p',
                        content: [
                            {
                            tag: 'label',
                            content: 'IP: ',
                        }, {
                            tag: 'label',
                            content: '{#node.model.IP}',
                        }
                        ],
                        props: {
                            "style": "font-size:80%;"
                        }
                    },{
                        tag: 'p',
                        content: [
                            {
                            tag: 'label',
                            content: 'Model: ',
                        }, {
                            tag: 'label',
                            content: '{#node.model.marca}',
                        }
                        ],
                        props: {
                            "style": "font-size:80%;"
                        }
                    }, 
                ],
                props: {
                    "style": "width: 150px;"
                }
            }]
            }
        });

        nx.define('Tooltip.Node', nx.ui.Component, {
            view: function(view){
                view.content.push({
                });
                return view;
            },
            methods: {
                attach: function(args) {
                    this.inherited(args);
                    this.model();
                }
            }
        });

        

        var currentLayout = 'auto'

        horizontal = function() {
            if (currentLayout === 'horizontal') {
                return;
            };
            currentLayout = 'horizontal';
            var layout = topo.getLayout('hierarchicalLayout');
            layout.direction('horizontal');
            layout.levelBy(function(node, model) {
                return model.get('layerSortPreference');
            });
            topo.activateLayout('hierarchicalLayout');
        };
        
        vertical = function() {
            if (currentLayout === 'vertical') {
                return;
            };
            currentLayout = 'vertical';
            var layout = topo.getLayout('hierarchicalLayout');
            layout.direction('vertical');
            layout.levelBy(function(node, model) {
            return model.get('layerSortPreference');
            });
            topo.activateLayout('hierarchicalLayout');
        }

        
        // Initialize topology
        var topo = new nx.graphic.Topology({
            width: 1500,
            height: 670,
            dataProcessor: 'force',
            identityKey: 'id',
            nodeConfig: {
                label: 'model.IP',
                iconType: 'model.icon',
                color: function(model) {
                    if (model.get('is_new') === 'yes') {
                        return '#148D09'; // Verde para nodos nuevos
                    }
                    if (model.get('is_dead') === 'yes') {
                        return '#E40039'; // Verde para nodos nuevos
                    }
                }
            },
            linkConfig: {
                linkType: 'curve', // Modificado para usar curvas
                sourcelabel: 'model.srcIfName',
                targetlabel: 'model.tgtIfName',
                style: function(model) {
                    if (model._data.is_dead === 'yes') {
                        // Los enlaces eliminados tienen el atributo 'is_dead' establecido en 'yes'
                        return { 'stroke-dasharray': '5' }; // Hacerlos discontinuos
                    }
                },
                color: function(model) {
                    if (model._data.is_dead === 'yes') {
                        // Los enlaces eliminados tienen el atributo 'is_dead' establecido en 'yes'
                        return '#E40039'; // Rojo
                    }
                    if (model._data.is_new === 'yes') {
                        // Los enlaces nuevos tienen el atributo 'is_new' establecido en 'yes'
                        return '#148D09'; // Verde
                    }
                },
            },
            showIcon: true,
            linkInstanceClass: 'CustomLinkClass', 
            tooltipManagerConfig: {
                nodeTooltipContentClass: 'CustomNodeTooltip'
            }
        });

        var Shell = nx.define(nx.ui.Application, {
            methods: {
                start: function () {
                    topo.data(topologyData);
                    topo.attach(this);
                }
            }
        });
        
        horizontal();
        var shell = new Shell();
        shell.start();
        document.getElementById('toggleLabelsButton').addEventListener('click', function() {
            showLabels = !showLabels; // Cambia el estado de visibilidad
            topo.eachLink(function(link) {
                link.update(); // Actualiza cada enlace para reflejar el cambio de visibilidad
            });

        });
    })(nx);
});