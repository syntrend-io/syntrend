# Syntrend CI Workflow

The overall branching convention uses Trunk-based development as this is releasing versioned products to external registries.

This requires that:

1. Each Feature and Bug being merged to `main` must by production ready.
2. Release Branches are created to...
  * allow cherry-picking of features/bugs to be included in a release.
  * isolate in-depth Release and UA Tests from an active `main` branch.

```mermaid
---
title: Branching Convention
config:
  gitGraph:
    showCommitLabel: false
---
gitGraph
    commit
    branch feat/new_feat
    commit
    checkout feat/new_feat
    commit
    commit
    checkout main
    commit
    branch bug/fix_issue
    checkout bug/fix_issue
    commit
    checkout feat/new_feat
    commit
    checkout main
    merge feat/new_feat
    checkout bug/fix_issue
    commit
    checkout main
    merge bug/fix_issue
    commit
    branch release/vX
    checkout release/vX
    commit tag:"vX"
    checkout main
    merge release/vX
```

## Branch Rules and Workflows

### Work Edits (commits)

Ensure no previously-require features/capabilities have been broken in the current work.

> [!NOTE]
> Objectives:
> 
> * be quick
> * includes unit/integration tests specific to the work being done
> * ensures no breaking changes to existing capabilities
> * can build a package

```mermaid
---
title: Commit Workflow
---
flowchart
    trCommit([Commit Trigger]) --> jbNewUnitTest[Identify and Run Work-specific Unit Tests]
    jbNewUnitTest --> jbUnitTests[Unit Tests]
    jbUnitTests --> jbBuildWheel[Build Wheel] & jbBuildDocker[Build Docker]
```

### Pull Requests

Should include everything necessary for the changes are production ready and can be included in a release.

> [!NOTE]
> Objectives:
> 
> * includes unit/integration/end-to-end tests specific to the work being done
> * ensures no breaking changes to existing capabilities
> * ensures no breaking changes after a merge to main (through a temporary branch with both branches)
> * can build a package and pushed to the target registries (as test builds)
> * passes all tests (end-to-end tests all performed on both Wheel and Docker builds)

```mermaid
---
title: PR Workflow
---
flowchart
    trCommit([PR Trigger]) --> jbNewUnitTest[Identify and Run Work-specific Tests]
    jbNewUnitTest --> jbUnitTests[Unit Tests] & jbIntegrationTests[Integration Tests]
    jbUnitTests & jbIntegrationTests --> jbReportCov[Code Coverage Report]
    jbReportCov --> jbBuildWheel[Build Wheel] & jbBuildDocker[Build Docker]
    jbBuildWheel & jbBuildDocker--> jbEndTests[End-to-End Tests]
    jbEndTests --> jbRegressionTests[Regression Tests]
    jbRegressionTests --> jbPublish[Publish Packages to Test Registries]
    jbPublish --> jbRemoveOldBuild[Remove old builds]
    jbPublish -.->|User Task| uat[User Acceptance]
    jbPublish -.->|Manual Trigger| jbTempBranch[Post-Merge Tests]
    jbTempBranch ~~~ n[Creates Temporary Branch\nwith main and the working branch\n\nRe-runs the PR Workflow\non the temporary branch]
    style n fill:#a82,color:#000
```

### Merge to Main

