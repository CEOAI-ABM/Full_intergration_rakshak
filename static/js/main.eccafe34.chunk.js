(this.webpackJsonpapp_one=this.webpackJsonpapp_one||[]).push([[0],{180:function(e,a){e.exports={savecampus:function(e){return{type:"CAMPUS_SAVE_DATA",data:e}},resetcampus:function(){return{type:"CAMPUS_RESET_DATA"}}}},187:function(e,a){e.exports={idReceive:function(e){return{type:"IO_STORE_ID",data:e}},simComplete:function(e){return{type:"IO_SIM_COMPLETE",data:e}}}},283:function(e,a){e.exports={saveScenarios:function(e){return{type:"SCENARIO_SAVE_DATA",data:e}},resetScenarios:function(){return{type:"SCENARIO_RESET_DATA"}}}},329:function(e,a,t){e.exports=t(577)},334:function(e,a,t){},335:function(e,a,t){},544:function(e,a){},550:function(e,a){},552:function(e,a){},577:function(e,a,t){"use strict";t.r(a);var n=t(0),r=t.n(n),i=t(15),o=t.n(i),c=(t(334),t(335),t(59),t(37)),l=t(38),s=t(42),m=t(40),u=t(56),p=t.n(u),d=t(49),b=t(19),y=t(12),h=t(622),E=t(630),f=t(47),g=t(32),v={totalSimulatedDays:5,populationDistribution:[{maxAge:5,probability:.131,deathRate:.01,incubationPeriod:6,probabilityOfSeverity:{mild:.7,mediocre:.26,severe:.04},probabilityOfComorbidity:0},{maxAge:18,probability:.242,deathRate:.005,incubationPeriod:6,probabilityOfSeverity:{mild:.8,mediocre:.16,severe:.04},probabilityOfComorbidity:0},{maxAge:25,probability:.126,deathRate:.01,incubationPeriod:8,probabilityOfSeverity:{mild:.95,mediocre:.04,severe:.01},probabilityOfComorbidity:0},{maxAge:60,probability:.346,deathRate:.01,incubationPeriod:5,probabilityOfSeverity:{mild:.6,mediocre:.3,severe:.1},probabilityOfComorbidity:0},{maxAge:80,probability:.075,deathRate:.04,incubationPeriod:2,probabilityOfSeverity:{mild:.4,mediocre:.4,severe:.2},probabilityOfComorbidity:0},{maxAge:150,probability:.08,deathRate:.3,incubationPeriod:2,probabilityOfSeverity:{mild:.1,mediocre:.4,severe:.5},probabilityOfComorbidity:0}],virusParameters:{r0:2,InitialTestingCapacampus:1e3,expectedDaysToCure:14,fullCapacampusRatio:{hospital:1.66,covidHealthCare:1.66,covidIsolationCentre:1.66},transportExposureParameter:{Time:2.2283,Distance:1},homeExposureParameter:{Time:16,Distance:1},groceryExposureParameter:{Time:.5,Distance:4},randomExposureParameter:{Time:1,Distance:2},unemployedExposureParameter:{Time:8,Distance:1}}},O=function(e,a){return"CAMPUS_SAVE_DATA"===a.type?Object(y.a)(Object(y.a)({},e),{},{campus:a.data,dayRange:[0,a.data.totalSimulatedDays]}):"CAMPUS_RESET_DATA"===a.type?Object(y.a)(Object(y.a)({},e),{},{campus:v,dayRange:[0,v.totalSimulatedDays]}):(console.log(a),console.warn("Action not recognized."),e)},C=t(180),j=t(647),D=t(626),S=t(629),N=t(106),A=t(652),_=t(181),P=t.n(_),R=t(637),x=t(646),k=t(132),T=t.n(k),w=t(81),I=t.n(w),W=t(182),V=t.n(W),G=t(631),H=t(632),M=t(633),z=t(651),U={virusParameters:"First add the R0 value for the virus you wish to simulate. Add initial testing capacampus and expected days to cure. The below listed exposure parameters contain expected time an Agent spends there, and the social distance he is able to maintain",fullCapacampusRatio:"The number of patients which each covid healtcare worker can handle successfully. In other words, bed capacampus per healtcare worker in different subclass of healthcare sectors"},L=Object(h.a)((function(e){return{root:{width:"95%",margin:"auto",padding:"1rem"},heading:{fontSize:e.typography.pxToRem(15),fontWeight:e.typography.fontWeightRegular}}}));function B(e){return e.replace(/([A-Z])/g," $1").replace(/^./,(function(e){return e.toUpperCase()}))}var F=function e(a){var t=a.schema,n=a.data,i=a.setData,o=a.name,c=a.display,l=a.format,s=void 0===l?B:l,m=a.arrayAction,u=void 0===m?void 0:m,p=Object.keys(t),d=L();return r.a.createElement("div",{className:d.accordionRoot},r.a.createElement(j.a,null,r.a.createElement(D.a,{expandIcon:r.a.createElement(P.a,null),"aria-controls":o+"-content",id:o+"-header"},r.a.createElement(N.a,{className:d.accordionHeading},s(o),U[o]?r.a.createElement(z.a,{title:r.a.createElement("div",{style:{fontSize:"1rem",padding:"0.5rem",lineHeight:"1.3rem"}},U[o]),placement:"right",style:{display:"inline-block",cursor:"pointer"},arrow:!0},r.a.createElement(V.a,{style:{fontSize:"1rem",color:"gray",marginLeft:"1rem"}})):r.a.createElement("div",null))),r.a.createElement(S.a,null,r.a.createElement("div",{style:{flexDirection:"column"}},p.map((function(a){return c(a)?Array.isArray(t[a])?r.a.createElement(j.a,null,r.a.createElement(D.a,{expandIcon:r.a.createElement(P.a,null),"aria-controls":o+"-"+a+"-content",id:o+"-"+a+"-header"},r.a.createElement(N.a,{className:d.accordionHeading},s(a),U[a]?r.a.createElement(z.a,{title:r.a.createElement("div",{style:{fontSize:"1rem",padding:"0.5rem",lineHeight:"1.3rem"}},U[a]),placement:"right",style:{display:"inline-block",cursor:"pointer"},arrow:!0},r.a.createElement(V.a,{style:{fontSize:"1rem",color:"gray",marginLeft:"1rem"}})):r.a.createElement("div",null))),r.a.createElement(S.a,{style:{flexDirection:"column"}},r.a.createElement(E.a,{variant:"contained",color:"primary",style:{width:"10px"}},r.a.createElement(T.a,{className:d.icon,onClick:function(){n[a].push(Object(f.cloneDeep)(t[a][0])),i()}})),n[a].map((function(l,m){return r.a.createElement(G.a,{className:d.cardRoot},r.a.createElement(H.a,{avatar:r.a.createElement(E.a,{variant:"contained",color:"secondary"},r.a.createElement(I.a,{className:d.icon,onClick:function(){n[a].splice(m,1),i()}})),title:s(a)+" "+String(m+1)}),r.a.createElement(M.a,null,r.a.createElement(e,{schema:t[a][0],data:l,name:"Parameters",format:s,display:c,setData:i}),void 0===u?r.a.createElement("div",{style:{display:"none"}}):r.a.createElement(E.a,{variant:"contained",color:"primary",id:"".concat(o,"-").concat(a,"-").concat(m,"-btn"),onClick:function(){u.call(l,m)}},u.content(l,m))))})))):"object"===typeof t[a]?r.a.createElement(e,{schema:t[a],data:n[a],format:s,name:a,display:c,setData:i}):"number"===typeof t[a]?r.a.createElement(A.a,{label:s(a),defaultValue:n[a],type:"number",InputLabelProps:{shrink:!0},onChange:function(e){n[a]=Number(e.target.value),i()}}):"string"===typeof t[a]?r.a.createElement(A.a,{label:s(a),defaultValue:n[a],type:"text",InputLabelProps:{shrink:!0},onChange:function(e){n[a]=String(e.target.value),console.log(n),i()}}):"boolean"===typeof t[a]?r.a.createElement(R.a,{control:r.a.createElement(x.a,{checked:n[a],name:o+"-"+a+"-checkbox",color:"primary"}),label:s(a),onChange:function(){n[a]=!n[a],i()}}):r.a.createElement("div",{style:{display:"none"}}):r.a.createElement("div",{style:{display:"none"}})}))))))},J=Object(h.a)((function(e){return{root:{width:"95%",margin:"auto",padding:"1rem"},heading:{fontSize:e.typography.pxToRem(15),fontWeight:e.typography.fontWeightRegular}}}));var K=Object(b.f)(Object(g.b)((function(e,a){return Object(y.a)(Object(y.a)({},a),{},{campus:e.campus})}))((function(e){var a=e.campus,t=e.history,n=e.dispatch,i=J(),o=Object(f.cloneDeep)(a);return r.a.createElement("div",{className:"form-container"},r.a.createElement("div",{style:{width:"90%",height:"90%",margin:"auto",padding:"2rem 0"}},r.a.createElement(F,{schema:v,data:o,name:"campus Parameters",display:function(e){return!0},setData:function(){n(Object(C.savecampus)(o))}}),r.a.createElement("div",{className:i.btnRoot},r.a.createElement(E.a,{variant:"contained",color:"primary",onClick:function(){n(Object(C.savecampus)(o)),t.push("/scenarios")}},"Save and Continue"))))}))),X=function(e){Object(s.a)(t,e);var a=Object(m.a)(t);function t(){return Object(c.a)(this,t),a.apply(this,arguments)}return Object(l.a)(t,[{key:"render",value:function(){return r.a.createElement("div",{className:"right-pane"},r.a.createElement("div",{className:"grad-bg"}),r.a.createElement(K,null))}}]),t}(r.a.Component),Y=function(e){Object(s.a)(t,e);var a=Object(m.a)(t);function t(){return Object(c.a)(this,t),a.apply(this,arguments)}return Object(l.a)(t,[{key:"render",value:function(){var e=this.props.color;return r.a.createElement("div",{className:"card"},r.a.createElement("p",null,this.props.title),r.a.createElement("div",{style:{position:"relative"}},r.a.createElement("h2",null,this.props.stats),r.a.createElement(p.a,{style:{position:"absolute",right:"0",top:"0",fontSize:"3rem",color:"lightblue"}})),r.a.createElement("p",{style:{color:e}},this.props.change,"%"),r.a.createElement("p",null,"Since ",this.props.duration))}}]),t}(r.a.Component),$=t(58),Z=Object(h.a)((function(e){return{root:{width:"95%",margin:"auto",padding:"1rem"},heading:{fontSize:e.typography.pxToRem(15),fontWeight:e.typography.fontWeightRegular},formControl:{margin:e.spacing(1),minWidth:120},selectEmpty:{marginTop:e.spacing(2)}}}));var q=Object(g.b)((function(e,a){return Object(y.a)(Object(y.a)(Object(y.a)({},e),a),{},{maxDay:e.campus.totalSimulatedDays})}))((function(e){var a=e.dispatch,t=(e.maxDay,e.simulationData),n=e.graphDisplay,i=e.dayRange,o=Z();return r.a.createElement("div",null,n.map((function(e,n){return r.a.createElement(G.a,null,r.a.createElement(H.a,{avatar:r.a.createElement(E.a,{variant:"contained",color:"secondary",style:{width:"10px"}},r.a.createElement(I.a,{className:o.icon,onClick:function(){a({type:"GRAPH_REMOVE_ONE",data:n})}})),title:"Graph ".concat(n+1)}),r.a.createElement(M.a,null,function(){var a=function(e){for(var a=[],n=function(n){var r={};e.forEach((function(e){r["Scenario-".concat(e.scenario," ").concat(e.column)]=Number(t[e.scenario][n][e.column])})),r.day=Number(t[e[0].scenario][n].DAY),a.push(r)},r=i[0];r<i[1];r++)n(r);return a}(e);return r.a.createElement($.d,{data:a,width:600,height:400,margin:{top:10,right:10,left:10,bottom:10}},r.a.createElement($.a,{strokeDasharray:"3.3"}),r.a.createElement($.e,null),r.a.createElement($.f,{dataKey:"day",label:"Day",type:"number",domain:i}),r.a.createElement($.g,null),r.a.createElement($.b,null),Object.keys(a[0]).map((function(e){return"day"!==e?r.a.createElement($.c,{type:"monotone",dataKey:e,stroke:"red",dot:{r:1}}):r.a.createElement("div",null)})))}()))})))})),Q=t(639),ee=t(643),ae=t(642),te=t(638),ne=t(640),re=t(641),ie=t(578),oe=Object(h.a)({table:{minWidth:650,backgroundColor:"rgba(0,0,0,1)",opacampus:.8},tableCell:{color:"white !important"}});function ce(e,a,t,n,r){return{name:e,calories:a,fat:t,carbs:n,protein:r}}var le=[ce("Frozen yoghurt",159,6,24,4),ce("Ice cream sandwich",237,9,37,4.3),ce("Eclair",262,16,24,6),ce("Cupcake",305,3.7,67,4.3),ce("Gingerbread",356,16,49,3.9)];function se(){var e=oe();return r.a.createElement(te.a,{component:ie.a},r.a.createElement(Q.a,{className:e.table,"aria-label":"simple table"},r.a.createElement(ne.a,null,r.a.createElement(re.a,null,r.a.createElement(ae.a,{className:e.tableCell,style:{fontWeight:"bold"}},"Dessert (100g serving)"),r.a.createElement(ae.a,{className:e.tableCell,style:{fontWeight:"bold"},align:"right"},"Calories"),r.a.createElement(ae.a,{className:e.tableCell,style:{fontWeight:"bold"},align:"right"},"Fat\xa0(g)"),r.a.createElement(ae.a,{className:e.tableCell,style:{fontWeight:"bold"},align:"right"},"Carbs\xa0(g)"),r.a.createElement(ae.a,{className:e.tableCell,style:{fontWeight:"bold"},align:"right"},"Protein\xa0(g)"))),r.a.createElement(ee.a,null,le.map((function(a){return r.a.createElement(re.a,{key:a.name},r.a.createElement(ae.a,{className:e.tableCell,component:"th",scope:"row"},a.name),r.a.createElement(ae.a,{className:e.tableCell,align:"right"},a.calories),r.a.createElement(ae.a,{className:e.tableCell,align:"right"},a.fat),r.a.createElement(ae.a,{className:e.tableCell,align:"right"},a.carbs),r.a.createElement(ae.a,{className:e.tableCell,align:"right"},a.protein))})))))}var me=t(649),ue=Object(h.a)({root:{width:240,color:"white",padding:"1.5rem",textAlign:"center",float:"right"}});function pe(e){return"".concat(e,"\xb0C")}var de=Object(g.b)((function(e,a){return Object(y.a)({maxDay:e.campus.totalSimulatedDays,value:e.dayRange},a)}))((function(e){var a=e.maxDay,t=e.value,n=e.dispatch,i=ue();return r.a.createElement("div",{className:i.root},r.a.createElement(N.a,{id:"range-slider",gutterBottom:!0},"Date Range"),r.a.createElement(me.a,{value:t,onChange:function(e,a){n({type:"GRAPH_CHANGE_RANGE",data:a})},valueLabelDisplay:"auto","aria-labelledby":"range-slider",getAriaValueText:pe,style:{color:"#5e72e4"},max:a}))})),be=t(103),ye=t(288),he=t(648),Ee=t(650),fe=t(636),ge=t(645),ve=Object(h.a)((function(e){return{root:{width:"95%",margin:"auto",padding:"1rem"},heading:{fontSize:e.typography.pxToRem(15),fontWeight:e.typography.fontWeightRegular},formControl:{margin:e.spacing(1),minWidth:120},selectEmpty:{marginTop:e.spacing(2)}}}));var Oe=Object(g.b)((function(e,a){return Object(y.a)(Object(y.a)({},a),{},{graphDisplay:e.graphDisplay,simulationData:e.simulationData})}))((function(e){var a=e.dispatch,t=(e.graphDisplay,e.simulationData),i=ve(),o={scenario:"",column:""},c=Object(n.useState)([o]),l=Object(ye.a)(c,2),s=l[0],m=l[1],u=function(e,a,t){var n=Object(be.a)(s);n[a][t]=e.target.value,m(n)};return r.a.createElement(G.a,null,r.a.createElement(H.a,{avatar:r.a.createElement(E.a,{variant:"contained",color:"primary",style:{width:"10px"}},r.a.createElement(T.a,{className:i.icon,onClick:function(){m([].concat(Object(be.a)(s),[Object(y.a)({},o)]))}})),title:"Add Columns to plot"}),r.a.createElement(M.a,null,s.map((function(e,a){return r.a.createElement("div",null,r.a.createElement(E.a,{variant:"contained",color:"primary",style:{width:"10px",borderRadius:5,backgroundColor:"red"}},r.a.createElement(I.a,{className:i.icon,onClick:function(){m(s.filter((function(e,t){return t!==a})))}})),r.a.createElement(fe.a,{className:i.formControl},r.a.createElement(he.a,{id:"scenario-selector"+a},"Scenario"),r.a.createElement(ge.a,{labelId:"scenario-selector"+a,id:"select-scenario-selector"+a,value:e.scenario,onChange:function(e){u(e,a,"scenario")}},Object.keys(t).map((function(e){return r.a.createElement(Ee.a,{value:e},e)})))),r.a.createElement(fe.a,{className:i.formControl},r.a.createElement(he.a,{id:"column-selector"+a},"Column"),r.a.createElement(ge.a,{labelId:"column-selector"+a,id:"select-column-selector"+a,value:e.column,onChange:function(e){u(e,a,"column")}},s[a].scenario in t?Object.keys(t[s[a].scenario][0]).map((function(e){return r.a.createElement(Ee.a,{value:e},e)})):r.a.createElement("div",null))))})),r.a.createElement(E.a,{variant:"contained",color:"primary",onClick:function(){var e=!0;s.forEach((function(a){""!==a.column&&""!==a.scenario||(e=!1)})),e?(a({type:"GRAPH_ADD_ONE",data:s}),m([o])):alert("Please set all values correctly")}},"Display Graph")))})),Ce=function(e){Object(s.a)(t,e);var a=Object(m.a)(t);function t(){return Object(c.a)(this,t),a.apply(this,arguments)}return Object(l.a)(t,[{key:"render",value:function(){return r.a.createElement("div",{className:"right-pane"},r.a.createElement("div",{className:"grad-bg"}),r.a.createElement("div",{className:"card-container",style:{display:"none"}},r.a.createElement(Y,{title:"traffic",stats:350897,change:3.48,duration:"last month",color:"lightgreen"}),r.a.createElement(Y,{title:"traffic",stats:350897,change:3.48,duration:"last month",color:"lightgreen"}),r.a.createElement(Y,{title:"traffic",stats:350897,change:3.48,duration:"last month",color:"lightgreen"}),r.a.createElement(Y,{title:"traffic",stats:350897,change:3.48,duration:"last month",color:"lightgreen"})),r.a.createElement("div",{className:"form-container"},r.a.createElement(Oe,null)),r.a.createElement("div",{className:"graph-container"},r.a.createElement(de,null),r.a.createElement(q,null)),r.a.createElement("div",{className:"table-container",style:{display:"none"}},r.a.createElement(se,null)))}}]),t}(r.a.Component),je=t(644),De=t(285),Se=t.n(De),Ne=t(283),Ae={scenarioDetails:[{ComplianceRate:.8}]},_e=function(e,a){return"SCENARIO_SAVE_DATA"===a.type?Object(y.a)(Object(y.a)({},e),{},{scenarios:a.data}):(console.log(a),console.warn("Action not recognized"),e)},Pe=t(284),Re=t.n(Pe),xe=t(187);function ke(e){var a={Virus_Deathrates:[],Virus_IncubationPeriod:[],Virus_ProbSeverity:[],Comorbidty_matrix:{ComorbidX:[]}};e.populationDistribution.forEach((function(e){a.Virus_Deathrates.push(e.deathRate),a.Virus_IncubationPeriod.push(e.incubationPeriod),a.Virus_ProbSeverity.push([e.probabilityOfSeverity.mild,e.probabilityOfSeverity.mediocre,e.probabilityOfSeverity.severe]),a.Comorbidty_matrix.ComorbidX.push(e.probabilityOfComorbidity)}));var t=e.virusParameters.fullCapacampusRatio;return a.Virus_FullCapRatio=[t.hospital,t.covidHealthCare,t.covidIsolationCentre],a.Virus_InitialTestingCap=e.virusParameters.initialTestingCapacampus,a.Virus_ExpectedCureDays=e.virusParameters.expectedDaysToCure,a.Virus_R0=e.virusParameters.r0,a.Virus_Prob_ContactTracing=e.virusParameters.probabilityOfContactTracing,a.Virus_Params={Transport:e.virusParameters.transportExposureParameter,Home:e.virusParameters.homeExposureParameter,Grocery:e.virusParameters.groceryExposureParameter,Unemployed:e.virusParameters.unemployedExposureParameter,Random:e.virusParameters.randomExposureParameter},a.SIMULATION_DAYS=e.totalSimulatedDays,a.Initial_Compliance_Rate=e.ComplianceRate,a}var Te;var we=Object(b.f)(Object(g.b)((function(e,a){return Object(y.a)(Object(y.a)({},e),a)}))((function(e){var a=e.campus,t=e.scenarios,n=e.simulations,i=e.dispatch,o=e.history,c=Object(f.cloneDeep)(t);return console.log(n),r.a.createElement("div",{className:"form-container"},r.a.createElement(F,{schema:Ae,data:c,name:"Scenarios",display:function(e){return!0},setData:function(){i(Object(Ne.saveScenarios)(c))},arrayAction:{content:function(e,a){return r.a.createElement("div",null,"Simulate",r.a.createElement(je.a,{color:"white",className:"progressbar",style:{display:a in n&&!1===n[a].complete?"block":"none"}}),r.a.createElement(Se.a,{className:"completeicon",style:{display:a in n&&!0===n[a].complete?"block":"none"}}))},call:function(e,t){!function(e,a,t){Te.emit("runsim",{caller:t,data:JSON.stringify(ke(Object(y.a)(Object(y.a)({},a),e)))})}(e,a,t)}}}),r.a.createElement(E.a,{variant:"contained",color:"primary",onClick:function(){o.push("/graphs")}},"Go to Graphs"))}))),Ie=function(e){Object(s.a)(t,e);var a=Object(m.a)(t);function t(){return Object(c.a)(this,t),a.apply(this,arguments)}return Object(l.a)(t,[{key:"render",value:function(){return r.a.createElement("div",{className:"right-pane"},r.a.createElement("div",{className:"grad-bg"}),r.a.createElement(we,null))}}]),t}(r.a.Component);function We(){return r.a.createElement("div",{className:"right-pane info-screen"},r.a.createElement("p",null,r.a.createElement("h3",null,"Welcome to the Covid-19 simulator in a self-customized IIT KGP Campus. Here you can play around by initializing your custom-tailored")))}var Ve=function(e){Object(s.a)(t,e);var a=Object(m.a)(t);function t(){return Object(c.a)(this,t),a.apply(this,arguments)}return Object(l.a)(t,[{key:"render",value:function(){return r.a.createElement(d.a,null,r.a.createElement(b.c,null,r.a.createElement(b.a,{exact:!0,path:"/",component:X}),r.a.createElement(b.a,{exact:!0,path:"/scenarios",component:Ie}),r.a.createElement(b.a,{exact:!0,path:"/graphs",component:Ce}),r.a.createElement(b.a,{exact:!0,path:"/info",component:We})),r.a.createElement("div",{className:"left-pane"},r.a.createElement("div",{className:"sideheader"},r.a.createElement("p",null,"Covid-19 Sim")),r.a.createElement("div",{className:"tablink"},r.a.createElement(p.a,null),r.a.createElement(d.b,{to:"/info"},"Instructions")),r.a.createElement("div",{className:"tablink"},r.a.createElement(p.a,null),r.a.createElement(d.b,{to:"/"},"campus Parameters")),r.a.createElement("div",{className:"tablink"},r.a.createElement(p.a,null),r.a.createElement(d.b,{to:"/scenarios"},"Scenarios")),r.a.createElement("div",{className:"tablink"},r.a.createElement(p.a,null),r.a.createElement(d.b,{to:"/graphs"},"Graphs")),r.a.createElement("div",{className:"tablink"},r.a.createElement(p.a,null),r.a.createElement(d.b,{to:"/maps"},"Maps")),r.a.createElement("div",{style:{width:"90%",height:"30px",borderBottom:"dotted 1px gray",margin:"0 auto 1rem"}})))}}]),t}(r.a.Component);var Ge=function(){return r.a.createElement("div",null,r.a.createElement(Ve,null))};Boolean("localhost"===window.location.hostname||"[::1]"===window.location.hostname||window.location.hostname.match(/^127(?:\.(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)){3}$/));var He=t(98),Me=t(286),ze=t.n(Me),Ue=function(e,a){if("IO_STORE_ID"===a.type){var t=Object(f.cloneDeep)(e);return t.simulations[a.data.caller]=a.data,t}if("IO_SIM_COMPLETE"===a.type){var n=Object(f.cloneDeep)(e);return n.simulations[a.data.caller].complete=!0,fetch("".concat("http://localhost:5000","/static/results/").concat(n.simulations[a.data.caller].id,"/CAMPUS_data.csv")).then((function(e){return e.text()})).then((function(e){ze.a.parse(e,{columns:!0},(function(e,t){n.simulationData[a.data.caller]=t}))})),n}return e};function Le(e,a){return"GRAPH_CHANGE_RANGE"===a.type?Object(y.a)(Object(y.a)({},e),{},{dayRange:a.data}):"GRAPH_ADD_ONE"===a.type?Object(y.a)(Object(y.a)({},e),{},{graphDisplay:[].concat(Object(be.a)(e.graphDisplay),[a.data])}):"GRAPH_REMOVE_ONE"===a.type?Object(y.a)(Object(y.a)({},e),{},{graphDisplay:e.graphDisplay.filter((function(e,t){return t!==a.data}))}):(console.log(a),console.warn("Action not recognised"),e)}var Be={campus:v,scenarios:Ae,simulations:{},dayRange:[0,v.totalSimulatedDays],simulationData:{},graphDisplay:[]};var Fe,Je=t(287),Ke=Object(He.createStore)((function(){var e=arguments.length>0&&void 0!==arguments[0]?arguments[0]:Be,a=arguments.length>1?arguments[1]:void 0;return a.type.startsWith("CAMPUS_")?O(e,a):a.type.startsWith("SCENARIO_")?_e(e,a):a.type.startsWith("IO_")?Ue(e,a):a.type.startsWith("GRAPH_")?Le(e,a):(console.log(a),console.warn("Action not recognized"),e)}),Object(Je.composeWithDevTools)()),Xe=(Fe=Ke.dispatch,(Te=Re()("http://localhost:5000")).on("sendid",(function(e){Fe(Object(xe.idReceive)(Object(y.a)(Object(y.a)({},e),{},{complete:!1})))})),Te.on("senddata",(function(e){console.log(e.log),-1!==e.log.indexOf("SIMULATION END")&&Fe(Object(xe.simComplete)(e))})),Te);o.a.render(r.a.createElement(r.a.StrictMode,null,r.a.createElement(g.a,{store:Ke},r.a.createElement(Ge,{connector:Xe}))),document.getElementById("root")),"serviceWorker"in navigator&&navigator.serviceWorker.ready.then((function(e){e.unregister()})).catch((function(e){console.error(e.message)}))},59:function(e,a,t){}},[[329,1,2]]]);
//# sourceMappingURL=main.eccafe34.chunk.js.map