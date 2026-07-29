import React, { useState } from 'react';
import { Navbar } from './components/Navbar';
import { HeroSection } from './components/HeroSection';
import { ChatBotDrawer } from './components/ChatBotDrawer';
import { OutageReportModal } from './components/OutageReportModal';
import { BillCalculatorModal } from './components/BillCalculatorModal';
import { MaintenanceSchedulerModal } from './components/MaintenanceSchedulerModal';
import { DisconnectionPolicySection } from './components/DisconnectionPolicySection';
import { OfficesSection } from './components/OfficesSection';
import { NotificationModal } from './components/NotificationModal';
import { CoreValuesFooter } from './components/CoreValuesFooter';
import { WaterWaveMotif } from './components/WaterWaveMotif';
import { HelmetIcon } from './components/HelmetIcon';
import { OutageNotice, OutageReport, MaintenanceRequest } from './types';
import { MessageSquare, AlertTriangle, Calculator, Wrench, ShieldCheck, MapPin, Clock, Droplets, ArrowRight, CheckCircle2 } from 'lucide-react';

export default function App() {
  // Modal & Drawer visibility states
  const [isChatOpen, setIsChatOpen] = useState(false);
  const [initialChatPrompt, setInitialChatPrompt] = useState<string | undefined>(undefined);
  
  const [isOutageModalOpen, setIsOutageModalOpen] = useState(false);
  const [isBillModalOpen, setIsBillModalOpen] = useState(false);
  const [isMaintenanceModalOpen, setIsMaintenanceModalOpen] = useState(false);
  const [isNotificationModalOpen, setIsNotificationModalOpen] = useState(false);

  // Active notices
  const [notices, setNotices] = useState<OutageNotice[]>([
    {
      id: 'not-1',
      parish: 'St. George',
      area: 'Grand Anse & Belmont',
      type: 'Unplanned Repair',
      status: 'In Progress',
      affecting: 'Temporary main line pressure reduction during valve replacement',
      estimatedResolution: 'Today, 2:30 PM',
      reportedAt: '8:15 AM',
      blueHelmetIcon: true,
    },
    {
      id: 'not-2',
      parish: 'St. Andrew',
      area: 'Grenville Town',
      type: 'Scheduled Maintenance',
      status: 'Dispatched',
      affecting: 'Network flushing on Victoria Street',
      estimatedResolution: 'Today, 4:00 PM',
      reportedAt: '9:00 AM',
      blueHelmetIcon: true,
    },
    {
      id: 'not-3',
      parish: 'Carriacou',
      area: 'Hillsborough',
      type: 'Water Pressure Recovery',
      status: 'Resolved',
      affecting: 'Storage tank supply restored',
      estimatedResolution: 'Completed',
      reportedAt: 'Yesterday',
      blueHelmetIcon: true,
    },
  ]);

  const [userReports, setUserReports] = useState<OutageReport[]>([]);
  const [userMaintenanceRequests, setUserMaintenanceRequests] = useState<MaintenanceRequest[]>([]);

  const handleOpenChatWithPrompt = (prompt: string) => {
    setInitialChatPrompt(prompt);
    setIsChatOpen(true);
  };

  const handleOutageSubmitSuccess = (report: OutageReport) => {
    setUserReports((prev) => [report, ...prev]);
  };

  const handleMaintenanceSubmitSuccess = (req: MaintenanceRequest) => {
    setUserMaintenanceRequests((prev) => [req, ...prev]);
  };

  return (
    <div className="min-h-screen flex flex-col bg-[#fafcff] text-slate-800 font-halis">
      
      {/* Top Navbar */}
      <Navbar
        onOpenNotifications={() => setIsNotificationModalOpen(true)}
        onOpenChat={() => handleOpenChatWithPrompt("Hello NAWASA assistant.")}
        onOpenOutageReport={() => setIsOutageModalOpen(true)}
        onOpenBillCalc={() => setIsBillModalOpen(true)}
        onOpenMaintenance={() => setIsMaintenanceModalOpen(true)}
        unreadCount={notices.length}
      />

      {/* Main Content Body */}
      <main className="flex-1">
        
        {/* Hero Section */}
        <HeroSection
          onOpenChatWithPrompt={handleOpenChatWithPrompt}
          onOpenOutageReport={() => setIsOutageModalOpen(true)}
          onOpenBillCalc={() => setIsBillModalOpen(true)}
          onOpenNotifications={() => setIsNotificationModalOpen(true)}
        />

        {/* Quick Utility Feature Cards Section */}
        <section className="py-16 bg-white relative">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 space-y-10">
            
            <div className="text-center max-w-3xl mx-auto space-y-2">
              <span className="text-xs font-bold uppercase tracking-wider text-[#0678ff] bg-[#0678ff]/10 px-3 py-1 rounded-full">
                Interactive Self-Service Hub
              </span>
              <h2 className="text-2xl sm:text-3xl font-extrabold text-slate-900">
                All NAWASA Customer Services at Your Fingertips
              </h2>
              <p className="text-sm text-slate-600">
                Access quick tools designed to make managing your water account effortless and transparent.
              </p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
              
              {/* Feature 1: AI Chatbot */}
              <div className="water-glass-card rounded-3xl p-6 border border-[#0678ff]/20 hover:border-[#0678ff] shadow-sm hover:shadow-md transition-all flex flex-col justify-between group">
                <div className="space-y-3">
                  <div className="w-12 h-12 rounded-2xl bg-[#0678ff] text-white flex items-center justify-center font-bold shadow-md group-hover:scale-110 transition-transform">
                    <MessageSquare className="w-6 h-6" />
                  </div>
                  <h3 className="text-lg font-extrabold text-slate-900">NAWASA AI Chat</h3>
                  <p className="text-xs text-slate-600 leading-relaxed">
                    24/7 intelligent answers on bills, payment channels, leak reports, and office times.
                  </p>
                </div>

                <button
                  onClick={() => handleOpenChatWithPrompt("What can NAWASA AI help me with?")}
                  className="mt-6 w-full py-2.5 rounded-xl bg-[#0678ff]/10 hover:bg-[#0678ff] text-[#0678ff] hover:text-white font-bold text-xs transition-colors flex items-center justify-center space-x-1"
                >
                  <span>Launch Chatbot</span>
                  <ArrowRight className="w-4 h-4" />
                </button>
              </div>

              {/* Feature 2: Outage & Burst Pipe */}
              <div className="bg-white rounded-3xl p-6 border border-slate-200 hover:border-[#fe8b02] shadow-sm hover:shadow-md transition-all flex flex-col justify-between group">
                <div className="space-y-3">
                  <div className="w-12 h-12 rounded-2xl bg-[#fe8b02]/10 text-[#fe8b02] flex items-center justify-center font-bold group-hover:scale-110 transition-transform">
                    <AlertTriangle className="w-6 h-6" />
                  </div>
                  <h3 className="text-lg font-extrabold text-slate-900">Report Burst Pipe</h3>
                  <p className="text-xs text-slate-600 leading-relaxed">
                    Report emergency leaks, no-water outages, or water discoloration for fast dispatch.
                  </p>
                </div>

                <button
                  onClick={() => setIsOutageModalOpen(true)}
                  className="mt-6 w-full py-2.5 rounded-xl bg-[#fe8b02]/10 hover:bg-[#fe8b02] text-[#fe8b02] hover:text-white font-bold text-xs transition-colors flex items-center justify-center space-x-1"
                >
                  <span>Open Report Form</span>
                  <ArrowRight className="w-4 h-4" />
                </button>
              </div>

              {/* Feature 3: Bill Estimator & Meter */}
              <div className="bg-white rounded-3xl p-6 border border-slate-200 hover:border-[#0678ff] shadow-sm hover:shadow-md transition-all flex flex-col justify-between group">
                <div className="space-y-3">
                  <div className="w-12 h-12 rounded-2xl bg-[#0678ff]/10 text-[#0678ff] flex items-center justify-center font-bold group-hover:scale-110 transition-transform">
                    <Calculator className="w-6 h-6" />
                  </div>
                  <h3 className="text-lg font-extrabold text-slate-900">Bill & Meter Guide</h3>
                  <p className="text-xs text-slate-600 leading-relaxed">
                    Estimate monthly charges, understand tariffs, and learn how to read your water meter.
                  </p>
                </div>

                <button
                  onClick={() => setIsBillModalOpen(true)}
                  className="mt-6 w-full py-2.5 rounded-xl bg-[#0678ff]/10 hover:bg-[#0678ff] text-[#0678ff] hover:text-white font-bold text-xs transition-colors flex items-center justify-center space-x-1"
                >
                  <span>Calculate Bill</span>
                  <ArrowRight className="w-4 h-4" />
                </button>
              </div>

              {/* Feature 4: Maintenance Scheduling */}
              <div className="bg-white rounded-3xl p-6 border border-slate-200 hover:border-[#4a8ae0] shadow-sm hover:shadow-md transition-all flex flex-col justify-between group">
                <div className="space-y-3">
                  <div className="w-12 h-12 rounded-2xl bg-[#4a8ae0]/10 text-[#4a8ae0] flex items-center justify-center font-bold group-hover:scale-110 transition-transform">
                    <Wrench className="w-6 h-6" />
                  </div>
                  <h3 className="text-lg font-extrabold text-slate-900">Maintenance Booking</h3>
                  <p className="text-xs text-slate-600 leading-relaxed">
                    Schedule meter testing, new connections, valve repairs, or view district flushing.
                  </p>
                </div>

                <button
                  onClick={() => setIsMaintenanceModalOpen(true)}
                  className="mt-6 w-full py-2.5 rounded-xl bg-[#4a8ae0]/10 hover:bg-[#4a8ae0] text-[#4a8ae0] hover:text-white font-bold text-xs transition-colors flex items-center justify-center space-x-1"
                >
                  <span>Schedule Service</span>
                  <ArrowRight className="w-4 h-4" />
                </button>
              </div>

            </div>

            {/* User Submitted Ticket Summary pill if any */}
            {(userReports.length > 0 || userMaintenanceRequests.length > 0) && (
              <div className="bg-slate-900 text-white rounded-2xl p-5 space-y-3 shadow-lg">
                <div className="flex items-center justify-between border-b border-slate-800 pb-2">
                  <h4 className="text-xs font-bold uppercase tracking-wider text-emerald-400">
                    Your Active Submitted Tickets
                  </h4>
                  <span className="text-[11px] text-slate-400">Saved locally</span>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-3 text-xs">
                  {userReports.map((rpt) => (
                    <div key={rpt.id} className="bg-slate-800 p-3 rounded-xl border border-slate-700 flex justify-between items-center">
                      <div>
                        <span className="font-bold text-[#fe8b02]">#{rpt.ticketNumber}</span>
                        <p className="text-slate-300 font-medium">{rpt.issueType} - {rpt.parish}</p>
                      </div>
                      <span className="bg-emerald-950 text-emerald-400 font-bold px-2 py-0.5 rounded text-[10px]">
                        {rpt.status}
                      </span>
                    </div>
                  ))}

                  {userMaintenanceRequests.map((req) => (
                    <div key={req.id} className="bg-slate-800 p-3 rounded-xl border border-slate-700 flex justify-between items-center">
                      <div>
                        <span className="font-bold text-[#0678ff]">#{req.ticketNumber}</span>
                        <p className="text-slate-300 font-medium">{req.serviceType} - {req.parish}</p>
                      </div>
                      <span className="bg-blue-950 text-blue-400 font-bold px-2 py-0.5 rounded text-[10px]">
                        {req.status}
                      </span>
                    </div>
                  ))}
                </div>
              </div>
            )}

          </div>
        </section>

        {/* Disconnection & Payment Plan Section */}
        <DisconnectionPolicySection
          onOpenChatWithPrompt={handleOpenChatWithPrompt}
        />

        {/* Offices & Opening Times Directory Section */}
        <OfficesSection
          onOpenChatWithPrompt={handleOpenChatWithPrompt}
        />

      </main>

      {/* Core Values Footer & Motto */}
      <CoreValuesFooter />

      {/* Modals & Drawers */}
      <ChatBotDrawer
        isOpen={isChatOpen}
        onClose={() => setIsChatOpen(false)}
        initialPrompt={initialChatPrompt}
        onTriggerOutageModal={() => setIsOutageModalOpen(true)}
        onTriggerBillModal={() => setIsBillModalOpen(true)}
      />

      <OutageReportModal
        isOpen={isOutageModalOpen}
        onClose={() => setIsOutageModalOpen(false)}
        onSubmitSuccess={handleOutageSubmitSuccess}
      />

      <BillCalculatorModal
        isOpen={isBillModalOpen}
        onClose={() => setIsBillModalOpen(false)}
        onOpenChatWithPrompt={handleOpenChatWithPrompt}
      />

      <MaintenanceSchedulerModal
        isOpen={isMaintenanceModalOpen}
        onClose={() => setIsMaintenanceModalOpen(false)}
        onSubmitSuccess={handleMaintenanceSubmitSuccess}
      />

      <NotificationModal
        isOpen={isNotificationModalOpen}
        onClose={() => setIsNotificationModalOpen(false)}
        notices={notices}
        onOpenChatWithPrompt={handleOpenChatWithPrompt}
      />

    </div>
  );
}
                            
Any questions you do not know the answer for should be replyed with "I am sorry, I do not have that information."
Use the following facts to answer user questions:
- NAWASA operates across the entire island of Grenada.
- NAWASA's mission is to  provide clean, safe, and reliable drinking water and efficient sewage services in a sustainable manner that exceeds customers' expectations.
- NAWASA's core values include excellence in operations and service delivery,social responsibility at the community and national levels, accountability at all levels to all stakeholders, innovation and creativity in operations and service delivery, outreaching and networking with stakeholders and having a culture of continuous improvement and a healthy working environment.
- NAWASA's email is communications@nawasa.gd.
- NAWASA's general opening hours include Mondays to Fridays: 8:00 a.m. to 4:00 p.m. 
- NAWASA's cash office opening hours include 7:30 a.m. to 3:00 p.m. for their main office and 8:00 a.m. to 3:00 p.m. for Grenville & Gouyave.
- NAWASA's Whatsapp numbers are 405 5245 / 459 6064 / 405 9143.
- New services should be installed within 10 working days after payment of connection fee.
- To change an account name, customers need to fill out the application for change of name form and provide at least one of the following documents, a title Deed/Conveyance, death Certificate, letter from Lawyer, will, or court Judgement.
- To change the billing/mailing address, the customer needs to fill out the "Change of Mailing Address Form"
- If a customer has been paying their bills, but their bill shows arrears it may mean that their current bill may have already been issued, prior to payment of their previous bill.
- High consumption may be attributable to a number of factors, such as estimated bills, leaks, unsecured taps which are easily accessible or a faulty meter. To determine whether the property has a leak, the customer must make sure that all taps are turned off, and then monitor the meter dial. A revolving meter indicates the presence of a leak.
- NAWASA effects disconnection of water services under circumstances such as, at the request of the customer, for non-payment of arrears, for wastage or abuse, illegal tampering of meters and other fittings.
- Requests for disconnection of service must be either made in writing or at NAWASA's office by filling out a "Request for disconnection" form. Such request can only be made by the owner of the account or duly authorized person (as per authorization documents). Valid Identification required.
- Customers are liable for disconnection for a minimum of $50.00, once that balance represents an amount which is at least 30 days in arrears.
- NAWASA reports to the Ministry of Health with regard to the quality of water given to consumers, moreover NAWASA is mandated by law ACT # 25 of 1990 to provide portable water to customers also by it mission statement which reads “To provide customer with a safe and adequate water supply safe disposal of waste water, in a viable and efficient manner that meet and exceed customer expectations, and ensure the development of our organization, communities and nation.
- NAWASA follows the World Health Organization (WHO) Guideline in treating water.
- Workers are given incentive after a given period of time.
- NAWASA means National Water & Sewerage Authority.
- NAWASA'smain office is located on the Carenage, but its facilities are spread throughout Grenada, Carriacou and Petit Martinique. Some of the sub offices are Gouyave, Grenville, Sauteurs St. David's and Grand Anse offices.
- The Owner of NAWASA is the Government of Grenada.
- The founder of NAWASA is the Government of Grenada.
- The motto of NAWASA is "Committed to Meeting Customers' Needs".
- NAWASA contributes to the development of Grenada. In fact all economics activities in Grenada depend on water to function. It is the main fuel that drives economic growth, some example of those sectors are Tourism, Construction, Agriculture both livestock and crop and Restaurant. Additionally, The National Water & Sewerage Authority (NAWASA) employs a large portion of the labour force it plays a part in contributing to the GDP of Grenada. Moreover, NAWASA in collaboration with the Government of Grenada to assist the under privilege persons by providing them with water connection and the Government pays the cost of connection and the water rates.
- Training for employees of NAWASA is done yearly.
- The National Water & Sewerage Authority (NAWASA) is a Public utility (operates as a Statutory body) - With a monopoly on the production and distribution of portable water and the collection and disposal of sewerage. Within the framework of its operation The National Water & Sewerage Authority (NAWASA) has a responsibility to provide a service to deprive communities and institutions to meet their need for water supply.
- NAWASA has Thirty (30) outlets for distribution including surface water treatment plants boreholes and desalination plants.
- NAWASA's water transportation is mainly through the pipeline, however water tanker is also use to transport water.  Other transportation used is mostly pickup vans to transport crew and tools, backhoes and trucks.
- NAWASA adopted this type of organizational structure as the structure is deemed appropriate based on the operations involve in providing the products and services:  Engineering Department, Human Resource, and Finance.
- 


Be helpful, concise, and polite. If a question is outside topics regarding NAWASA, steer them back warmly.
