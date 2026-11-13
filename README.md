# Cardiac Digital Twin Personalization Pipeline | Documentation & Deployment

This repository contains the documentation and deployment files for the **Cardiac Digital Twin Personalization Pipeline*** implemented for the Master Thesis: _"Implementation of a pipeline to generate a patient-specific Digital Twin of Cardiac Electrophysiology"_

## System Architecture

The pipeline implements an end-to-end containerized software architecture for constructing and personalizing a Patient-Specific Digital Twin of Cardiac Electrophysiology from clinical data (CMR imaging and 12-lead ECG).

## Components Repositories
The pipeline integrates heterogeneous software components, available at the following repositories:

- [biv-me](https://github.com/FedeOmb/biv-me) - **Anatomical Twinning** - reconstruction of 3D biventricular cardiac geometries from CMR DICOMS

- [Cobiveco](https://github.com/FedeOmb/Cobiveco) - **Anatomical Twinning** - computation of Cobiveco ventricular coordinates and cardiac fibers orientation 

- [TORSO-MPP](https://github.com/FedeOmb/TORSO-MPP) - **Anatomical Twinning** - estimation of 12-lead ECG electrodes position from CMR scout views

- [Cardiac-Digital-Twin](https://github.com/FedeOmb/Cardiac-Digital-Twin) - **Functional Twinning** - SMC-ABC inference framework and monodomain translation to Opencarp

## Deployment

## Pipeline Workflow

