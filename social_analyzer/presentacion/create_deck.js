const pptxgen = require('pptxgenjs');

const pptx = new pptxgen();
pptx.layout = 'LAYOUT_WIDE';
pptx.author = 'Grupo Redes';
pptx.subject = 'Exposición final PRAC4';
pptx.title = 'Analizador de Redes Sociales · v1.0.0';
pptx.company = 'Técnicas de Programación Avanzada';
pptx.lang = 'es-ES';
pptx.theme = {
  headFontFace: 'Georgia', bodyFontFace: 'Calibri', lang: 'es-ES'
};
pptx.defineLayout({ name: 'LAYOUT_WIDE', width: 13.333, height: 7.5 });
pptx.layout = 'LAYOUT_WIDE';

const C = {
  ink: '0F172A', slate: '334155', muted: '64748B', paper: 'F8FAFC', white: 'FFFFFF',
  teal: '0F766E', mint: '2DD4BF', pale: 'CCFBF1', coral: 'F97316', sand: 'FFF7ED',
  line: 'CBD5E1', green: '16A34A', red: 'DC2626'
};
const W = 13.333, H = 7.5;
const shadow = () => ({ type: 'outer', color: '0F172A', blur: 3, angle: 45, distance: 1, opacity: 0.12 });

function addSlideNumber(slide, n, dark=false) {
  slide.addText(String(n).padStart(2, '0'), { x: 12.35, y: 7.05, w: 0.45, h: 0.2, fontFace: 'Calibri', fontSize: 9, color: dark ? '94A3B8' : C.muted, align: 'right', margin: 0 });
}
function addTitle(slide, title, kicker, dark=false) {
  if (kicker) slide.addText(kicker.toUpperCase(), { x: 0.72, y: 0.42, w: 3.8, h: 0.22, fontFace: 'Calibri', fontSize: 10, bold: true, charSpacing: 1.6, color: dark ? C.mint : C.teal, margin: 0 });
  slide.addText(title, { x: 0.72, y: 0.78, w: 11.7, h: 0.55, fontFace: 'Georgia', fontSize: 28, bold: true, color: dark ? C.white : C.ink, margin: 0, breakLine: false, fit: 'shrink' });
}
function addNetwork(slide, x, y, scale=1, dark=false) {
  const nodes = [[0.3,1.0],[1.5,0.2],[2.7,0.9],[1.0,2.1],[2.35,2.35],[3.35,1.7]];
  const edges = [[0,1],[0,3],[1,2],[1,3],[2,4],[2,5],[3,4],[4,5]];
  edges.forEach(([a,b]) => {
    const A=nodes[a], B=nodes[b];
    slide.addShape(pptx.ShapeType.line, { x:x+(A[0]+0.11)*scale, y:y+(A[1]+0.11)*scale, w:(B[0]-A[0])*scale, h:(B[1]-A[1])*scale, line:{ color: dark ? '475569' : '99F6E4', width:1.6 } });
  });
  nodes.forEach((p,i)=>slide.addShape(pptx.ShapeType.ellipse,{x:x+p[0]*scale,y:y+p[1]*scale,w:0.24*scale,h:0.24*scale,fill:{color:i===2?C.coral:(dark?C.mint:C.teal)},line:{color:dark?C.ink:C.paper,width:1}}));
}
function addCard(slide, x,y,w,h,title,body,accent=C.teal) {
  slide.addShape(pptx.ShapeType.roundRect,{x,y,w,h,rectRadius:0.08,fill:{color:C.white},line:{color:C.line,width:1},shadow:shadow()});
  slide.addShape(pptx.ShapeType.ellipse,{x:x+0.28,y:y+0.28,w:0.38,h:0.38,fill:{color:accent},line:{color:accent}});
  slide.addText(title,{x:x+0.82,y:y+0.24,w:w-1.05,h:0.3,fontFace:'Calibri',fontSize:17,bold:true,color:C.ink,margin:0});
  slide.addText(body,{x:x+0.28,y:y+0.86,w:w-0.56,h:h-1.08,fontFace:'Calibri',fontSize:12.5,color:C.slate,margin:0.02,breakLine:false,fit:'shrink',valign:'top'});
}
function addArrow(slide,x,y,w,color=C.teal){
  slide.addShape(pptx.ShapeType.chevron,{x,y,w,h:0.52,fill:{color},line:{color},adjustPoint:0.55});
}

// 1. Portada
{
  const s=pptx.addSlide(); s.background={color:C.ink};
  s.addText('ANALIZADOR DE\nREDES SOCIALES',{x:0.78,y:1.15,w:7.2,h:1.7,fontFace:'Georgia',fontSize:38,bold:true,color:C.white,margin:0,breakLine:false,fit:'shrink'});
  s.addText('Entrega final · PRAC4 · v1.0.0',{x:0.82,y:3.12,w:5.6,h:0.36,fontFace:'Calibri',fontSize:18,bold:true,color:C.mint,margin:0});
  s.addText('De un CSV a información útil, local y reproducible.',{x:0.82,y:3.72,w:6.2,h:0.4,fontFace:'Calibri',fontSize:20,color:'CBD5E1',margin:0});
  s.addText('Carlos Anguita · Javier del Pozo · Nicolás García · Quanan Wei',{x:0.82,y:6.55,w:8.6,h:0.28,fontFace:'Calibri',fontSize:11,color:'94A3B8',margin:0});
  addNetwork(s,8.3,1.12,1.18,true); addSlideNumber(s,1,true);
  s.addNotes('[0:00-0:30] Presentar al equipo y el objetivo. Mensaje clave: la versión 1.0.0 cierra un flujo completo, local y reproducible; no intenta resolver análisis semántico ni grandes volúmenes.');
}

// 2. Problema y solución
{
  const s=pptx.addSlide(); s.background={color:C.paper}; addTitle(s,'Del fichero bruto a una salida explicable','Problema y solución');
  const xs=[0.75,3.52,6.29,9.06];
  const data=[['1','Importar','CSV UTF-8 validado'],['2','Persistir','SQLite transaccional'],['3','Analizar','Participación, temas y tiempo'],['4','Exportar','JSON y CSV abiertos']];
  data.forEach((d,i)=>{
    s.addShape(pptx.ShapeType.roundRect,{x:xs[i],y:2.05,w:2.22,h:2.55,rectRadius:0.06,fill:{color:i===3?C.sand:C.white},line:{color:i===3?C.coral:C.line,width:1.2},shadow:shadow()});
    s.addText(d[0],{x:xs[i]+0.28,y:2.3,w:0.55,h:0.58,fontFace:'Georgia',fontSize:30,bold:true,color:i===3?C.coral:C.teal,margin:0});
    s.addText(d[1],{x:xs[i]+0.28,y:3.08,w:1.66,h:0.32,fontFace:'Calibri',fontSize:18,bold:true,color:C.ink,margin:0});
    s.addText(d[2],{x:xs[i]+0.28,y:3.62,w:1.66,h:0.64,fontFace:'Calibri',fontSize:13,color:C.slate,margin:0,fit:'shrink'});
    if(i<3) addArrow(s,xs[i]+2.34,3.05,0.74,i===2?C.coral:C.teal);
  });
  s.addText('Privacidad por diseño: los datos permanecen en el equipo.',{x:0.82,y:5.42,w:7.3,h:0.36,fontFace:'Calibri',fontSize:18,bold:true,color:C.teal,margin:0});
  s.addText('Alcance explícito: CSV + SQLite + análisis determinista.',{x:0.82,y:5.98,w:7.4,h:0.3,fontFace:'Calibri',fontSize:14,color:C.muted,margin:0});
  addNetwork(s,9.6,5.05,0.65,false); addSlideNumber(s,2);
  s.addNotes('[0:30-1:15] Recorrer las cuatro etapas en una frase cada una. Resaltar que las salidas son abiertas y que no se envían datos a servicios externos.');
}

// 3. Arquitectura
{
  const s=pptx.addSlide(); s.background={color:C.paper}; addTitle(s,'Capas pequeñas, responsabilidades claras','Arquitectura');
  const boxes=[
    {x:0.8,y:2.58,w:1.72,t:'CSV',c:C.pale},{x:3.0,y:1.55,w:2.2,t:'Importador\n(ABC)',c:'DDF4FF'},
    {x:3.0,y:3.52,w:2.2,t:'CLI',c:C.sand},{x:5.75,y:2.53,w:2.3,t:'Conversación\n(dominio)',c:'ECFCCB'},
    {x:8.55,y:1.3,w:2.7,t:'Analizador\n(fachada)',c:'EDE9FE'},{x:8.55,y:3.05,w:2.7,t:'Repositorio\nSQLite',c:'E0F2FE'},
    {x:8.55,y:4.8,w:2.7,t:'Reporting\nJSON / CSV',c:'FFEDD5'}
  ];
  boxes.forEach(b=>{s.addShape(pptx.ShapeType.roundRect,{x:b.x,y:b.y,w:b.w,h:0.95,rectRadius:0.05,fill:{color:b.c},line:{color:C.line,width:1}});s.addText(b.t,{x:b.x+0.12,y:b.y+0.16,w:b.w-0.24,h:0.58,fontFace:'Calibri',fontSize:16,bold:true,color:C.ink,align:'center',valign:'mid',margin:0,fit:'shrink'});});
  [[2.52,3.04,0.44,0],[5.23,2.72,0.48,0],[8.08,2.72,0.44,-0.92],[8.08,2.83,0.44,0.67],[8.08,2.98,0.44,2.1],[4.1,2.5,0,-0.92]].forEach((e,i)=>s.addShape(pptx.ShapeType.line,{x:e[0],y:e[1],w:e[2],h:e[3],line:{color:i===5?C.coral:C.teal,width:2,beginArrowType:'none',endArrowType:'triangle'}}));
  s.addShape(pptx.ShapeType.roundRect,{x:5.62,y:5.58,w:5.86,h:0.7,rectRadius:0.04,fill:{color:C.ink},line:{color:C.ink}});
  s.addText('Dominio sin dependencias de CSV, SQLite, argparse ni formatos de informe',{x:5.9,y:5.8,w:5.3,h:0.26,fontFace:'Calibri',fontSize:13,bold:true,color:C.white,align:'center',margin:0});
  s.addText('Extensible sin sacrificar simplicidad',{x:0.82,y:5.68,w:3.8,h:0.44,fontFace:'Georgia',fontSize:22,bold:true,color:C.teal,margin:0});
  addSlideNumber(s,3);
  s.addNotes('[1:15-2:30] Empezar en CSV y seguir las flechas. Explicar herencia/polimorfismo en Importador, composición en Analizador y cierre transaccional en RepositorioSQLite. Terminar con el desacoplamiento del dominio.');
}

// 4. Calidad
{
  const s=pptx.addSlide(); s.background={color:C.paper}; addTitle(s,'Calidad medible antes de la demo','Pruebas y CI');
  const stats=[['20','pruebas locales\nsuperadas'],['≥70 %','umbral de\ncobertura'],['1','flujo de integración\ncompleto'],['3 SO','Windows · macOS\nLinux']];
  stats.forEach((d,i)=>{
    const x=0.78+i*3.08;
    s.addShape(pptx.ShapeType.roundRect,{x,y:1.75,w:2.55,h:2.28,rectRadius:0.06,fill:{color:i===1?C.ink:C.white},line:{color:i===1?C.ink:C.line,width:1},shadow:shadow()});
    s.addText(d[0],{x:x+0.22,y:2.05,w:2.11,h:0.75,fontFace:'Georgia',fontSize:34,bold:true,color:i===1?C.mint:(i===2?C.coral:C.teal),align:'center',margin:0});
    s.addText(d[1],{x:x+0.25,y:3.0,w:2.05,h:0.65,fontFace:'Calibri',fontSize:14,bold:true,color:i===1?C.white:C.slate,align:'center',margin:0,fit:'shrink'});
  });
  const steps=['validar','importar','persistir','analizar','exportar','eliminar'];
  steps.forEach((t,i)=>{
    const x=0.88+i*2.05;
    s.addShape(pptx.ShapeType.roundRect,{x,y:5.2,w:1.56,h:0.66,rectRadius:0.04,fill:{color:i===5?C.sand:C.pale},line:{color:i===5?C.coral:C.teal,width:1}});
    s.addText(t,{x:x+0.08,y:5.41,w:1.4,h:0.22,fontFace:'Calibri',fontSize:12,bold:true,color:i===5?C.coral:C.teal,align:'center',margin:0});
    if(i<steps.length-1) s.addShape(pptx.ShapeType.line,{x:x+1.56,y:5.53,w:0.49,h:0,line:{color:C.line,width:2,endArrowType:'triangle'}});
  });
  s.addText('Integración: una sola prueba cruza todas las capas',{x:0.9,y:6.2,w:5.3,h:0.26,fontFace:'Calibri',fontSize:14,bold:true,color:C.ink,margin:0}); addSlideNumber(s,4);
  s.addNotes('[2:30-3:15] Distinguir: 20 pruebas pasaron en la preparación local sin el plugin de cobertura; la CI instala pytest-cov y exige al menos 70 %. Señalar el recorrido de la prueba de integración.');
}

// 5. Demo inicio
{
  const s=pptx.addSlide(); s.background={color:C.ink}; addTitle(s,'Una orden, el flujo completo','Demo · parte 1',true);
  s.addShape(pptx.ShapeType.roundRect,{x:0.78,y:1.7,w:7.45,h:3.98,rectRadius:0.04,fill:{color:'020617'},line:{color:'334155',width:1.2}});
  s.addText('PS> python scripts/demo.py',{x:1.08,y:2.0,w:6.8,h:0.42,fontFace:'Consolas',fontSize:19,bold:true,color:C.mint,margin:0});
  const lines=['analizador-redes 1.0.0','CSV válido: 3 mensajes, 2 participantes','Conversación importada con id 1','1   Demo PRAC4   3 mensajes','Informe guardado en build/demo/resumen.json'];
  lines.forEach((t,i)=>s.addText(t,{x:1.08,y:2.7+i*0.55,w:6.68,h:0.28,fontFace:'Consolas',fontSize:13,color:i===4?'FBBF24':'CBD5E1',margin:0}));
  const cmds=[['01','Versión'],['02','Validación'],['03','Importación'],['04','Listado']];
  cmds.forEach((d,i)=>{const y=1.75+i*1.12;s.addShape(pptx.ShapeType.ellipse,{x:9.12,y,w:0.58,h:0.58,fill:{color:i===3?C.coral:C.teal},line:{color:i===3?C.coral:C.teal}});s.addText(d[0],{x:9.21,y:y+0.18,w:0.4,h:0.14,fontFace:'Calibri',fontSize:9,bold:true,color:C.white,align:'center',margin:0});s.addText(d[1],{x:9.92,y:y+0.13,w:2.0,h:0.28,fontFace:'Calibri',fontSize:17,bold:true,color:C.white,margin:0});});
  s.addText('No depende de rutas específicas de Windows o macOS.',{x:8.98,y:6.35,w:3.55,h:0.42,fontFace:'Calibri',fontSize:13,color:'94A3B8',margin:0,fit:'shrink'}); addSlideNumber(s,5,true);
  s.addNotes('[3:15-4:35] Cambiar a la terminal y ejecutar python scripts/demo.py. No narrar cada línea: confirmar versión, validación e id persistido. Si la demo falla, continuar con esta captura simulada y abrir los artefactos ya generados.');
}

// 6. Demo resultado
{
  const s=pptx.addSlide(); s.background={color:C.paper}; addTitle(s,'El resultado es legible y reutilizable','Demo · parte 2');
  s.addShape(pptx.ShapeType.roundRect,{x:0.78,y:1.62,w:6.25,h:4.88,rectRadius:0.04,fill:{color:'F1F5F9'},line:{color:C.line,width:1}});
  const json=['{','  "total_mensajes": 3,','  "total_participantes": 2,','  "participacion": [...],','  "temas": [...],','  "actividad_por_fecha": {...}','}'];
  json.forEach((t,i)=>s.addText(t,{x:1.12,y:1.98+i*0.52,w:5.55,h:0.3,fontFace:'Consolas',fontSize:15,color:i===1||i===2?C.coral:C.slate,bold:i===1||i===2,margin:0}));
  addCard(s,7.6,1.7,4.65,1.3,'Participación','Volumen, porcentaje y longitud media por usuario.',C.teal);
  addCard(s,7.6,3.25,4.65,1.3,'Temas frecuentes','Términos normalizados, explicables y reproducibles.',C.coral);
  addCard(s,7.6,4.8,4.65,1.3,'Actividad temporal','Agrupación por fecha y hora para detectar patrones.',C.green);
  s.addText('JSON para análisis · CSV para interoperabilidad',{x:0.95,y:6.72,w:6.2,h:0.25,fontFace:'Calibri',fontSize:13,bold:true,color:C.teal,margin:0}); addSlideNumber(s,6);
  s.addNotes('[4:35-6:00] Abrir build/demo/resumen.json. Señalar únicamente tres bloques: participación, temas y actividad. Evitar leer el JSON completo. Mostrar que también existe mensajes.csv y volver a las diapositivas.');
}

// 7. Feedback
{
  const s=pptx.addSlide(); s.background={color:C.paper}; addTitle(s,'Consolidar antes que complicar','Feedback PRAC3 → decisión PRAC4');
  addCard(s,0.78,1.72,3.72,2.08,'Fortalezas confirmadas','Arquitectura coherente, persistencia robusta, código claro y pruebas de comportamientos completos.',C.green);
  addCard(s,4.82,1.72,3.72,2.08,'Riesgo identificado','Crecer con métricas o formatos adicionales sin una necesidad clara podía introducir complejidad innecesaria.',C.coral);
  addCard(s,8.86,1.72,3.72,2.08,'Decisión final','Cerrar release, elevar el umbral, publicar docs, automatizar demo y comprobar los tres sistemas operativos.',C.teal);
  s.addShape(pptx.ShapeType.roundRect,{x:1.55,y:4.75,w:10.22,h:1.12,rectRadius:0.06,fill:{color:C.ink},line:{color:C.ink}});
  s.addText('“Priorizar la calidad frente al crecimiento innecesario de funcionalidades”',{x:2.0,y:5.04,w:9.32,h:0.45,fontFace:'Georgia',fontSize:22,italic:true,color:C.white,align:'center',margin:0,fit:'shrink'});
  s.addText('La limitación también es una decisión de diseño.',{x:4.1,y:6.22,w:5.2,h:0.32,fontFace:'Calibri',fontSize:16,bold:true,color:C.teal,align:'center',margin:0}); addSlideNumber(s,7);
  s.addNotes('[6:00-7:00] Atribuir esta orientación al feedback de seguimiento. Explicar que no añadir JSON de entrada o NLP no es una carencia oculta: son extensiones futuras explícitas.');
}

// 8. Lecciones
{
  const s=pptx.addSlide(); s.background={color:C.paper}; addTitle(s,'Cuatro aprendizajes que sí trasladamos','Lecciones aprendidas');
  const items=[
    ['01','Diseñar fronteras','El dominio mejora cuando ignora detalles de entrada y almacenamiento.'],
    ['02','Probar comportamientos','Una integración completa aporta más confianza que pruebas aisladas sin contexto.'],
    ['03','Cerrar recursos','Las transacciones y conexiones deben probarse también en escenarios de error.'],
    ['04','Documentar lo real','Diferenciar claramente lo implementado de lo previsto evita expectativas falsas.']
  ];
  items.forEach((it,i)=>{const x=i%2===0?0.82:6.78;const y=i<2?1.72:4.12;s.addShape(pptx.ShapeType.roundRect,{x,y,w:5.72,h:1.82,rectRadius:0.05,fill:{color:i===3?C.sand:C.white},line:{color:i===3?C.coral:C.line,width:1},shadow:shadow()});s.addText(it[0],{x:x+0.28,y:y+0.28,w:0.7,h:0.45,fontFace:'Georgia',fontSize:24,bold:true,color:i===3?C.coral:C.teal,margin:0});s.addText(it[1],{x:x+1.18,y:y+0.26,w:4.1,h:0.34,fontFace:'Calibri',fontSize:18,bold:true,color:C.ink,margin:0});s.addText(it[2],{x:x+1.18,y:y+0.82,w:4.08,h:0.58,fontFace:'Calibri',fontSize:12.5,color:C.slate,margin:0,fit:'shrink'});});
  addSlideNumber(s,8);
  s.addNotes('[7:00-8:15] Repartir una lección entre distintos miembros si participa todo el grupo. Vincular cada aprendizaje con una evidencia concreta del proyecto, sin ampliar el alcance.');
}

// 9. Cierre
{
  const s=pptx.addSlide(); s.background={color:C.ink};
  s.addText('v1.0.0',{x:0.82,y:0.9,w:2.5,h:0.42,fontFace:'Calibri',fontSize:18,bold:true,color:C.mint,margin:0});
  s.addText('LISTO PARA\nENTREGAR Y DEMOSTRAR',{x:0.82,y:1.58,w:7.35,h:1.65,fontFace:'Georgia',fontSize:34,bold:true,color:C.white,margin:0,fit:'shrink'});
  const checks=['Flujo funcional cerrado','Pruebas + integración','Docs API generables','Demo y guion preparados'];
  checks.forEach((t,i)=>{const y=3.85+i*0.58;s.addShape(pptx.ShapeType.ellipse,{x:0.88,y,w:0.28,h:0.28,fill:{color:C.mint},line:{color:C.mint}});s.addText('✓',{x:0.91,y:y+0.03,w:0.22,h:0.15,fontFace:'Calibri',fontSize:9,bold:true,color:C.ink,align:'center',margin:0});s.addText(t,{x:1.35,y:y-0.02,w:3.7,h:0.28,fontFace:'Calibri',fontSize:16,color:C.white,margin:0});});
  addNetwork(s,8.3,1.42,1.15,true);
  s.addShape(pptx.ShapeType.roundRect,{x:8.45,y:5.3,w:3.95,h:0.86,rectRadius:0.05,fill:{color:C.coral},line:{color:C.coral}});
  s.addText('Preguntas',{x:8.75,y:5.57,w:3.35,h:0.28,fontFace:'Georgia',fontSize:22,bold:true,color:C.white,align:'center',margin:0});
  s.addText('Gracias',{x:0.84,y:6.82,w:2.0,h:0.28,fontFace:'Calibri',fontSize:13,color:'94A3B8',margin:0}); addSlideNumber(s,9,true);
  s.addNotes('[8:15-9:00] Cerrar con la versión, no con una lista de futuras funcionalidades. Recordar que la etiqueta se crea tras CI verde y que contribuciones/coevaluación requieren datos reales del grupo. Abrir preguntas.');
}

pptx.writeFile({ fileName: 'PRAC4_Exposicion_Final.pptx' });
