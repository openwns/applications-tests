##############################################################################
# This file is part of openWNS (open Wireless Network Simulator)
# _____________________________________________________________________________
#
# Copyright (C) 2004-2007
# Chair of Communication Networks (ComNets)
# Kopernikusstr. 5, D-52074 Aachen, Germany
# phone: ++49-241-80-27910,
# fax: ++49-241-80-22242
# email: info@openwns.org
# www: http://www.openwns.org
# _____________________________________________________________________________
#
# openWNS is free software; you can redistribute it and/or modify it under the
# terms of the GNU Lesser General Public License version 2 as published by the
# Free Software Foundation;
#
# openWNS is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
###############################################################################

### applicationsTestsSimpleTL
# Applications over UDP and SimpleTL
import openwns
import openwns.qos
import openwns.evaluation.default
# import other modules to be loaded
import simpleTL.Component
import openwns.distribution

import applications.clientSessions
import applications.serverSessions

import applications.component
import applications.evaluation.default

# create an instance of the WNS configuration
simulation = openwns.Simulator(simulationModel = openwns.node.NodeSimulationModel()) #wns.WNS.WNS()
simulation.outputStrategy = openwns.simulator.OutputStrategy.DELETE
# simulation duration
simulation.maxSimTime = 10.0
# simulation.fastShutdown = False
simulation.probesWriteInterval = 60 # in seconds realTime

numberOfClientNodes = 1
numberOfServerNodes = 1
numberOfStations = numberOfClientNodes

# link speed = 1 GBit/s
speed = 100E3
# Traffic load
meanPacketSize = 1500 * 8
loadFactor = 0.1
throughputPerStation = speed * loadFactor / numberOfStations
# evaluation start Time
settlingTime = 0.1

simulation.modules.simpletl.channel.capacity = speed

class ServerNode(openwns.node.Node):
    tl = None
    #applications = None
    load = None
    logger = None
    def __init__(self, id):
        super(ServerNode, self).__init__("Server"+str(id))
        self.logger = openwns.logger.Logger("APPL", "Server"+str(id), True) # used for Component
        self.load = applications.component.Server(self, "applications", self.logger)   
        # create Components in a server node
        self.tl = simpleTL.Component.Component(self, "ServerTL", "137.226.4."+str(id))

class ClientNode(openwns.node.Node):
    tl = None
    load = None
    logger = None
    def __init__(self, id):
        super(ClientNode, self).__init__("Client"+str(id))
        self.logger = openwns.logger.Logger("APPL", "Client"+str(id), True) # used for Component
        self.load = applications.component.Client(self, "applications", self.logger)
        # create Components in a client node
        self.tl = simpleTL.Component.Component(self, "ClientTL", "127.0.0."+str(id))


# installing servers
serverIdList = []
for j in xrange(numberOfServerNodes):
    node = ServerNode(j*(numberOfClientNodes+1)+1)
    ipaddress = "127.0.0." + str(j+1)
    logger = node.logger
    startTime = 0.01 # [s]
    phaseDuration = simulation.maxSimTime
    duration = phaseDuration - startTime
    serverIdList.append(j+1)

    cbr = applications.serverSessions.CBR(packetSize = 512, bitRate = 64, parentLogger = logger)
    tlListenerBinding = applications.component.TLListenerBinding(node.tl.domainName, ipaddress, 1024, openwns.qos.undefinedQosClass, 1024, cbr, logger)
    node.load.addListenerBinding(tlListenerBinding)

    email = applications.serverSessions.Email(meanOfNumberOfEmails = 30.0, sigmaOfNumberOfEmails = 17.0, medianOfLargeEmailSize = 227.0, sigmaOfLargeEmailSize = 1.0, valueOfLargeEmailSize = 928331.2, medianOfSmallEmailSize = 22.7, sigmaOfSmallEmailSize = 1.0, valueOfSmallEmailSize = 9286.11, parentLogger = logger)
    tlListenerBinding = applications.component.TLListenerBinding(node.tl.domainName, ipaddress, 1025, openwns.qos.undefinedQosClass, 1025, email, logger)
    node.load.addListenerBinding(tlListenerBinding)

    ftp = applications.serverSessions.FTP(parentLogger = logger)
    tlListenerBinding = applications.component.TLListenerBinding(node.tl.domainName, ipaddress, 1026, openwns.qos.undefinedQosClass, 1026, ftp, logger)
    node.load.addListenerBinding(tlListenerBinding)

    video = applications.serverSessions.Video(frameGenProcess = 'P-FARIMA', genreChoice = 'Movies', codecChoice = 'MPEG4', formatChoice = 'CIF', qualityChoice = '040404', parentLogger = logger)
    tlListenerBinding = applications.component.TLListenerBinding(node.tl.domainName, ipaddress, 1027, openwns.qos.undefinedQosClass, 1027, video, logger)
    node.load.addListenerBinding(tlListenerBinding)

    voip = applications.serverSessions.VoIP(codecType = applications.codec.AMR_12_2(), comfortNoiseChoice = True, parentLogger = logger)
    tlListenerBinding = applications.component.TLListenerBinding(node.tl.domainName, ipaddress, 1028, openwns.qos.undefinedQosClass, 1028, voip, logger)
    node.load.addListenerBinding(tlListenerBinding)

    videotelephony = applications.serverSessions.VideoTelephony(voiceCodecType = applications.codec.GSM(), comfortNoiseChoice = True, videoCodecType = 'MPEG4', videoFormatType = 'QCIF', videoQualityChoice = '040404', parentLogger = logger)
    tlListenerBinding = applications.component.TLListenerBinding(node.tl.domainName, ipaddress, 1029, openwns.qos.undefinedQosClass, 1029, videotelephony, logger)
    node.load.addListenerBinding(tlListenerBinding)
    
    videotrace = applications.serverSessions.VideoTrace(genreChoice = 'Movies', codecChoice = 'MPEG4', formatChoice = 'QCIF', rateControlChoice = 'VBR', qualityChoice = '30-30-30', parentLogger = logger)
    tlListenerBinding = applications.component.TLListenerBinding(node.tl.domainName, ipaddress, 1030, openwns.qos.undefinedQosClass, 1030, videotrace, logger)
    node.load.addListenerBinding(tlListenerBinding)
    
    www = applications.serverSessions.WWW(meanSizeOfMainObject = 10710.0, sigmaOfMainObjectSize = 158.22, meanSizeOfEmbeddedObject = 7758.0, sigmaOfEmbeddedObjectSize = 355.2, parentLogger = logger)
    tlListenerBinding = applications.component.TLListenerBinding(node.tl.domainName, ipaddress, 1031, openwns.qos.undefinedQosClass, 1031, www, logger)
    node.load.addListenerBinding(tlListenerBinding)
    
    wimaxvideo = applications.serverSessions.WiMAXVideo(framesPerSecond = 10.0, numberOfPackets = 8.0, shapeOfPacketSize = 1.2, scaleOfPacketSize = 40.0 , shapeOfPacketIat = 1.2, scaleOfPacketIat = 2.5, parentLogger = logger)
    tlListenerBinding = applications.component.TLListenerBinding(node.tl.domainName, ipaddress, 1032, openwns.qos.undefinedQosClass, 1032, wimaxvideo, logger)
    node.load.addListenerBinding(tlListenerBinding)
    
    wimaxvideotelephony = applications.serverSessions.WiMAXVideoTelephony(codecType = applications.codec.GSM(), comfortNoiseChoice = True, framesPerSecond = 25.0, scaleOfIFrame = 5.15, shapeOfIFrame = 863.0, shiftOfIFrameSize = 3949.0, meanOfBFrameSize = 147.0, sigmaOfBFrameSize = 74.0, meanOfPFrameSize = 259.0, sigmaOfPFrameSize = 134.0, parentLogger = logger)
    tlListenerBinding = applications.component.TLListenerBinding(node.tl.domainName, ipaddress, 1033, openwns.qos.undefinedQosClass, 1033, wimaxvideotelephony, logger)
    node.load.addListenerBinding(tlListenerBinding)
    
    simulation.simulationModel.nodes.append(node)
        
    # installing clients
    clientIdList = []
    for i in xrange(numberOfClientNodes):
        node = ClientNode((i+1)+(j*(numberOfClientNodes+1))+1)
        logger = node.logger
        ipaddress = "137.226.4."+str(j*(numberOfClientNodes+1)+1)
        clientIdList.append(i+numberOfServerNodes+1)

        cbr = applications.clientSessions.CBR(packetSize = 512, bitRate = 64, parentLogger = logger)
        tlBinding = applications.component.TLBinding(node.tl.domainName, ipaddress, 1024, openwns.qos.undefinedQosClass, 1024, logger)
        node.load.addTraffic(tlBinding, cbr)

        email = applications.clientSessions.Email(meanOfNumberOfEmails = 14.0, sigmaOfNumberOfEmails = 12.0, medianOfLargeEmailSize = 227.0, sigmaOfLargeEmailSize = 1.0, valueOfLargeEmailSize = 928331.2, medianOfSmallEmailSize = 22.7, sigmaOfSmallEmailSize = 1.0, valueOfSmallEmailSize = 9286.11, shapeOfEmailReadingTime = 1.1, scaleOfEmailReadingTime = 2.0, shapeOfEmailWritingTime = 1.1, scaleOfEmailWritingTime = 2.0, parentLogger = logger)
        tlBinding = applications.component.TLBinding(node.tl.domainName, ipaddress, 1025, openwns.qos.undefinedQosClass, 1025, logger)
        node.load.addTraffic(tlBinding, email)
    
        ftp = applications.clientSessions.FTP(meanOfReadingTime = 180.0, meanOfAmountOfData = 2.0, sigmaOfAmountOfData = 0.722, parentLogger = logger)
        tlBinding = applications.component.TLBinding(node.tl.domainName, ipaddress, 1026, openwns.qos.undefinedQosClass, 1026, logger)
        node.load.addTraffic(tlBinding, ftp)
    
        video = applications.clientSessions.Video(parentLogger = logger)
        tlBinding = applications.component.TLBinding(node.tl.domainName, ipaddress, 1027, openwns.qos.undefinedQosClass, 1027, logger)
        node.load.addTraffic(tlBinding, video)

        voip = applications.clientSessions.VoIP(codecType = applications.codec.AMR_12_2(), comfortNoiseChoice = True, parentLogger = logger)
        tlBinding = applications.component.TLBinding(node.tl.domainName, ipaddress, 1028, openwns.qos.undefinedQosClass, 1028, logger)
        node.load.addTraffic(tlBinding, voip)

        videotelephony = applications.clientSessions.VideoTelephony(voiceCodecType = applications.codec.GSM(), comfortNoiseChoice = True, videoCodecType = 'MPEG4', formatType = 'QCIF', qualityChoice = '040404', parentLogger = logger)
        tlBinding = applications.component.TLBinding(node.tl.domainName, ipaddress, 1029, openwns.qos.undefinedQosClass, 1029, logger)
        node.load.addTraffic(tlBinding, videotelephony)

        videotrace = applications.clientSessions.VideoTrace(genreChoice = 'Movies', codecChoice = 'MPEG4', formatChoice = 'QCIF', rateControlChoice = 'VBR', qualityChoice = '30-30-30', parentLogger = logger)
        tlBinding = applications.component.TLBinding(node.tl.domainName, ipaddress, 1030, openwns.qos.undefinedQosClass, 1030, logger)
        node.load.addTraffic(tlBinding, videotrace)
    
        www = applications.clientSessions.WWW(meanOfReadingTime = 30.0, meanOfParsingTime = 0.13, shapeOfEmbeddedObjects = 1.1, scaleOfEmbeddedObjects = 2.0, parentLogger = logger)
        tlBinding = applications.component.TLBinding(node.tl.domainName, ipaddress, 1031, openwns.qos.undefinedQosClass,  1031, logger)
        node.load.addTraffic(tlBinding, www)
    
        wimaxvideo = applications.clientSessions.WiMAXVideo(parentLogger = logger)
        tlBinding = applications.component.TLBinding(node.tl.domainName, ipaddress, 1032, openwns.qos.undefinedQosClass, 1032, logger)
        node.load.addTraffic(tlBinding, wimaxvideo)
    
        wimaxvideotelephony = applications.clientSessions.WiMAXVideoTelephony(codecType = applications.codec.GSM(), comfortNoiseChoice = True, framesPerSecond = 25.0, scaleOfIFrame = 5.15, shapeOfIFrame = 863.0, shiftOfIFrameSize = 3949.0, meanOfBFrameSize = 147.0, sigmaOfBFrameSize = 74.0, meanOfPFrameSize = 259.0, sigmaOfPFrameSize = 134.0, parentLogger = logger)
        tlBinding = applications.component.TLBinding(node.tl.domainName, ipaddress, 1033, openwns.qos.undefinedQosClass, 1033, logger)
        node.load.addTraffic(tlBinding, wimaxvideotelephony)
    
        simulation.simulationModel.nodes.append(node)

# installing probes

sesTypes = ['CBR', 'Email', 'FTP', 
            'VoIP', 'Video', 'VideoTelephony', 
            'VideoTrace', 'WWW', 'WiMAXVideo', 
            'WiMAXVideoTelephony']

applications.evaluation.default.installEvaluation(simulation, serverIdList + clientIdList, 
    sesTypes, settlingTime)
openwns.evaluation.default.installEvaluation(simulation)

openwns.setSimulator(simulation)











