import React, { useMemo, useState } from 'react';
import { createRoot } from 'react-dom/client';
import { Activity, AlertTriangle, Bot, CheckCircle2, Clock3, GitBranch, Layers3, LockKeyhole, Network, PlayCircle, Repeat2, Rocket, Workflow } from 'lucide-react';
import { Area, AreaChart, Bar, BarChart, CartesianGrid, Line, LineChart, ResponsiveContainer, Tooltip, XAxis, YAxis } from 'recharts';
import './styles.css';

const pages = ['Overview', 'Workflow Builder', 'Run Console', 'Agent Registry', 'Approvals', 'Retries', 'Audit Logs', 'Analytics'];
const runTrend = [{d:'Mon',runs:42,success:39,failed:3},{d:'Tue',runs:48,success:45,failed:3},{d:'Wed',runs:55,success:51,failed:4},{d:'Thu',runs:61,success:58,failed:3},{d:'Fri',runs:74,success:71,failed:3}];
const agents = [
  ['research_agent','knowledge retrieval','active','143 tasks'],
  ['analysis_agent','reasoning and scoring','active','211 tasks'],
  ['approval_agent','human gate routing','watch','37 tasks'],
  ['execution_agent','tool execution','active','184 tasks']
];
const audit = [
  ['09:10','RUN-8812','workflow accepted','orchestrator'],
  ['09:11','RUN-8812','research task completed','research_agent'],
  ['09:12','RUN-8812','approval gate requested','approval_agent'],
  ['09:18','RUN-8812','execution resumed','operator']
];
const approvals = [
  ['APR-118','vendor payout workflow','Finance approval','pending'],
  ['APR-119','customer notification workflow','Legal review','approved'],
  ['APR-120','data export workflow','Security approval','pending']
];

function fallbackRun(form){
  const hasApproval = form.tasks.toLowerCase().includes('approval') || form.tasks.toLowerCase().includes('payment');
  const taskCount = form.tasks.split('\n').filter(Boolean).length || 3;
  return { run_id:`RUN-${Date.now().toString().slice(-5)}`, status: hasApproval ? 'waiting_approval' : 'completed', total_tasks: taskCount, duration_ms: hasApproval ? 1840 : 970, environment: form.environment, orchestrator_version:'flowpilot-v1.1', steps: ['parse workflow DAG','resolve dependencies','assign specialized agents', hasApproval ? 'pause at approval gate' : 'execute all tasks','write audit events'], recommended_action: hasApproval ? 'Review pending approval gate before continuing execution.' : 'Workflow completed successfully. Review audit events and output bundle.' };
}

function App(){
  const [active,setActive] = useState('Overview');
  const [form,setForm] = useState({ workflow_name:'Enterprise onboarding automation', environment:'prod', tasks:'ingest customer profile\nretrieve policy documents\nscore account risk\nrequest approval\nexecute welcome workflow' });
  const [run,setRun] = useState(fallbackRun(form));
  const metrics = useMemo(()=>[
    ['Workflow Runs','14.8K','+28%',Workflow],['Success Rate','96.1%','+4.2%',CheckCircle2],['Avg Duration','970ms','-19%',Clock3],['Agent Tasks','54K','+31%',Bot]
  ],[]);
  const execute = async()=>{
    try{
      const response = await fetch('/workflows/run',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({name:form.workflow_name,environment:form.environment,tasks:form.tasks.split('\n').filter(Boolean).map((name,index)=>({id:`task_${index+1}`,name,agent:'execution_agent',depends_on:index?[`task_${index}`]:[] }))})});
      if(!response.ok) throw new Error('offline');
      setRun(await response.json());
    }catch{setRun(fallbackRun(form));}
  };
  return <main className="app-shell"><aside className="sidebar"><div className="brand"><Network/><div><strong>FlowPilot AI</strong><span>Autonomous Workflow Cloud</span></div></div>{pages.map(p=><button className={active===p?'active':''} onClick={()=>setActive(p)} key={p}>{p}</button>)}</aside><section className="workspace"><header className="topbar"><div><p className="eyebrow">Agentic workflow orchestration</p><h1>{active}</h1></div><button onClick={execute}>Run workflow</button></header>{active==='Overview'&&<Overview metrics={metrics}/>} {active==='Workflow Builder'&&<WorkflowBuilder form={form} setForm={setForm} run={run} execute={execute}/>} {active==='Run Console'&&<RunConsole run={run}/>} {active==='Agent Registry'&&<AgentRegistry/>} {active==='Approvals'&&<Approvals/>} {active==='Retries'&&<Retries/>} {active==='Audit Logs'&&<AuditLogs/>} {active==='Analytics'&&<Analytics/>}</section></main>
}
function Overview({metrics}){return <><section className="metrics">{metrics.map(([l,v,d,Icon])=><article className="card" key={l}><Icon/><span>{l}</span><strong>{v}</strong><small>{d}</small></article>)}</section><section className="grid"><Panel title="Run volume" icon={<Activity/>}><ResponsiveContainer width="100%" height={260}><AreaChart data={runTrend}><CartesianGrid strokeDasharray="3 3" stroke="#26374a"/><XAxis dataKey="d" stroke="#9badc1"/><YAxis stroke="#9badc1"/><Tooltip/><Area dataKey="runs" stroke="#38bdf8" fill="#0e7490"/></AreaChart></ResponsiveContainer></Panel><Panel title="Success vs failure" icon={<GitBranch/>}><ResponsiveContainer width="100%" height={260}><BarChart data={runTrend}><XAxis dataKey="d" stroke="#9badc1"/><YAxis stroke="#9badc1"/><Tooltip/><Bar dataKey="success" fill="#22c55e"/><Bar dataKey="failed" fill="#fb7185"/></BarChart></ResponsiveContainer></Panel></section></>}
function WorkflowBuilder({form,setForm,run,execute}){return <section className="grid"><Panel title="Workflow designer" icon={<Layers3/>}><label>Workflow name<input value={form.workflow_name} onChange={e=>setForm({...form,workflow_name:e.target.value})}/></label><label>Environment<input value={form.environment} onChange={e=>setForm({...form,environment:e.target.value})}/></label><label>Tasks<textarea value={form.tasks} onChange={e=>setForm({...form,tasks:e.target.value})}/></label><button onClick={execute}>Execute workflow</button></Panel><Panel title="DAG preview" icon={<GitBranch/>}>{form.tasks.split('\n').filter(Boolean).map((task,i)=><div className="node" key={task}><span>Task {i+1}</span><strong>{task}</strong><small>{i?'depends on previous task':'root task'}</small></div>)}<div className={`status ${run.status}`}>{run.status}</div></Panel></section>}
function RunConsole({run}){return <section className="grid"><Panel title="Run summary" icon={<PlayCircle/>}><div className="score"><span className={run.status}>{run.status}</span><strong>{run.run_id}</strong><p>{run.total_tasks} tasks · {run.duration_ms}ms · {run.environment}</p><small>{run.orchestrator_version}</small></div><div className="reason">{run.recommended_action}</div></Panel><Panel title="Execution steps" icon={<Workflow/>}>{(run.steps||[]).map(step=><div className="reason" key={step}>{step}</div>)}</Panel></section>}
function AgentRegistry(){return <Panel title="Specialized agents" icon={<Bot/>}><Table rows={agents}/></Panel>}
function Approvals(){return <section className="grid"><Panel title="Approval gates" icon={<LockKeyhole/>}><Table rows={approvals}/></Panel><Panel title="Governance policy" icon={<CheckCircle2/>}><div className="reason">Payments require finance approval.</div><div className="reason">External customer messages require supervisor review.</div><div className="reason">Sensitive data exports require security approval.</div></Panel></section>}
function Retries(){return <section className="grid"><Panel title="Retry controls" icon={<Repeat2/>}><div className="reason">Transient tool failures retry up to 3 times.</div><div className="reason">Dead-letter queue captures repeated failures.</div><div className="reason">Human operator can resume from failed task.</div></Panel><Panel title="Failure signals" icon={<AlertTriangle/>}><div className="reason">API timeout on execution_agent task.</div><div className="reason">Approval gate expired after SLA window.</div><div className="reason">Dependency result missing for downstream task.</div></Panel></section>}
function AuditLogs(){return <Panel title="Workflow audit stream" icon={<Activity/>}><Table rows={audit}/></Panel>}
function Analytics(){return <section className="grid"><Panel title="Throughput analytics" icon={<Rocket/>}><ResponsiveContainer width="100%" height={260}><LineChart data={runTrend}><XAxis dataKey="d" stroke="#9badc1"/><YAxis stroke="#9badc1"/><Tooltip/><Line dataKey="runs" stroke="#38bdf8" strokeWidth={3}/><Line dataKey="success" stroke="#22c55e" strokeWidth={3}/></LineChart></ResponsiveContainer></Panel><Panel title="Optimization insights" icon={<Activity/>}><div className="reason">Approval gates create 42% of total run latency.</div><div className="reason">Execution agent has highest task volume.</div><div className="reason">Workflow success rate improved after retry policy tuning.</div></Panel></section>}
function Table({rows}){return <div className="table">{rows.map(row=><div className="row" key={row.join('-')}>{row.map(cell=><span key={cell}>{cell}</span>)}</div>)}</div>}
function Panel({title,icon,children}){return <article className="panel"><div className="panel-title">{icon}<h2>{title}</h2></div>{children}</article>}

createRoot(document.getElementById('root')).render(<App/>);
