# How to Use the Senior Secops Skill

## Quick Start

Hey Claude—I just added the "senior-secops" skill. Can you perform a security assessment?

## Example Invocations

### Example 1: Basic Usage
```
Hey Claude—I just added the "senior-secops" skill. Can you perform a security assessment?
```

### Example 2: Specific Workflow
```
Hey Claude—I just added the "senior-secops" skill. Can you help me with perform security scan and vulnerability assessment?
```

### Example 3: Integration with Other Skills
```
Hey Claude—I just added the "senior-secops" skill. Can you use it together with related skills to deliver a complete solution?
```

## What to Provide

When using this skill, provide:

- **System Details**: Infrastructure overview, technology stack
- **Context** (optional): Compliance requirements, threat model
- **Scope** (optional): Specific areas to focus on, known vulnerabilities

## What You'll Get

This skill will provide:

- **Security Assessment**: Vulnerability analysis, risk assessment
- **Remediation Plan**: Prioritized action items with implementation guidance
- **Compliance Report**: Gap analysis against security standards
- **Automated Tools**: 3 Python scripts for data processing and analysis

## Python Tools Available

This skill includes the following Python tools:

- **compliance_checker.py**: Compliance Checker
- **security_scanner.py**: Security Scanner
- **vulnerability_assessor.py**: Vulnerability Assessor

You can run these tools directly:

```bash
python skills/engineering-team/senior-secops/scripts/compliance_checker.py --help
```

## Tips for Best Results

1. **Be Specific**: Provide clear, detailed requirements for better results
2. **Provide Context**: Include relevant background information about your project
3. **Iterate**: Start with a focused request, then refine based on initial results
4. **Combine Skills**: This skill works well with other engineering skills for comprehensive solutions

## Related Skills

Consider using these skills together:

- **[Senior Security](../../engineering-team/senior-security/)**: Complementary expertise for senior security tasks
- **[Senior Frontend](../../engineering-team/senior-frontend/)**: Complementary expertise for senior frontend tasks
- **[Cto Advisor](../../engineering-team/cto-advisor/)**: Complementary expertise for cto advisor tasks

---

**Skill**: senior-secops
**Domain**: engineering-team
**Version**: 1.0.0
**Last Updated**: 2025-11-23
