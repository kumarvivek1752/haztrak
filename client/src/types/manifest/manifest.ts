import { RejectionInfo } from 'components/ManifestForm/manifestSchema';
import { RcraLocality, Handler, Transporter, Signer } from 'types/site';
import { WasteLine } from 'types/wasteLine';
import { AdditionalInfo, CorrectionInfo, CorrectionRequest } from 'types/manifest';
import { z } from 'zod';

const mtnDetailsSchema = z.object({
  manifestTrackingNumber: z.string(),
  status: z.string(),
});

/**
 * Select details about a manifest for display, navigation, and analysis.
 * Often used in composite types (arrays).
 */
export type MtnDetails = z.infer<typeof mtnDetailsSchema>;

/**
 * The Manifest, also known as hazardous waste manifest, is a key component of the
 * United States Environmental Protection Agency's (US EPA) hazardous waste tracking
 * program. It captures information on the type and quantity of waste being transported,
 * instructions for handling, and custody exchange data (signatures).
 */
export interface Manifest {
  createdDate?: string;
  updatedDate?: string;
  /**
   * A unique alphanumeric identifier for assigned to each hazardous waste manifest.
   * It can only be created/assigned by EPA or authorized paper manifest printers
   * Expected format: 9 digits followed by suffix containing 3 upper case letters. [0-9]{9}[A-Z]{3}
   */
  manifestTrackingNumber?: string;
  status?:
    | 'NotAssigned'
    | 'Pending'
    | 'Scheduled'
    | 'InTransit'
    | 'ReadyForSignature'
    | 'Signed'
    | 'Corrected'
    | 'UnderCorrection'
    | 'MtnValidationFailed';
  isPublic?: boolean;
  /**
   * Manifest types are categorized by how they are submitted to EPA.
   * https://www.epa.gov/e-manifest/frequent-questions-about-e-manifest#fac_question1
   */
  submissionType?: 'FullElectronic' | 'DataImage5Copy' | 'Hybrid' | 'Image';
  /**
   * Indicates if a manifest was signed by TSDF (it has been received and submitted)
   */
  signatureStatus?: boolean;
  /**
   * Specifies how the manifest was created.
   * Mail is a legacy option for when mailed paper manifest were accepted by EPA.
   */
  originType?: 'Web' | 'Service' | 'Mail';
  shippedDate?: string;
  potentialShipDate: string;
  /**
   * The date the manifest was received by EPA
   */
  receivedDate?: string;
  certifiedDate?: string;
  certifiedBy?: Signer;
  /**
   * The handler that generated the hazardous waste
   */
  generator: Handler;
  /**
   * One or more handlers responsible for carrying the hazardous waste from the generator to the
   * designated receiving facility.
   */
  transporters: Array<Transporter>;
  /**
   * The hazardous waste handler responsible for treating, storing,
   * or disposing of the hazardous waste.
   */
  designatedFacility: Handler;
  broker?: Handler;
  /**
   * One or more lines on the manifest, each corresponding to a hazardous waste stream
   * and its relevant information.
   */
  wastes: Array<WasteLine>;
  /**
   * True is the hazardous waste was rejected by the designated receiving facility
   */
  rejection: boolean;
  rejectionInfo?: RejectionInfo;
  /**
   * True if there is a discrepancy between the waste information listed on the manifest and
   * what is actually transported.
   */
  discrepancy?: boolean;
  residue?: boolean;
  residueNewManifestTrackingNumber?: string[];
  /**
   * True if the hazardous waste shipment was imported from a foreign country
   */
  import?: boolean;
  /**
   * Relevant info on imported waste(s)
   */
  importInfo?: ImportInfo;
  correctionRequests?: CorrectionRequest[];
  containsPreviousRejectOrResidue: boolean;
  printedDocument?: Document;
  formDocument?: Document;
  additionalInfo?: AdditionalInfo;
  correctionInfo?: CorrectionInfo;
  /**
   * The status of the manifest if it's being transcribed by the EPA's Paper Processing Center (PPC)
   */
  ppcStatus?:
    | 'Draft'
    | 'PendingDataEntry'
    | 'DataEntryInProgress'
    | 'PendingDataQc'
    | 'PendingDataQa'
    | 'DataQaCompleted';
  // mtnValidationInfo
  provideImageGeneratorInfo?: boolean;
  /**
   * True if the manifest is locked for further editing.
   * A manifest will remain locked until the necessary modifications are complete.
   */
  locked: boolean;
  lockReason?: 'AsyncSign' | 'EpaChangeBiller' | 'EpaCorrection';
}

/**
 * Details required if the hazardous waste is internationally imported
 */
interface ImportInfo {
  importGenerator: Handler;
  portOfEntry: PortOfEntry;
}

/**
 * Location info on imported waste
 */
interface PortOfEntry {
  state: RcraLocality;
  cityPort: string;
}

/**
 * Metadata for the manifest file (PDFs, HTML)
 */
interface Document {
  name: string;
  size: number;
  mimeType: 'APPLICATION_PDF' | 'TEXT_HTML';
}
